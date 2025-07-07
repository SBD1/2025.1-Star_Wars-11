"""merge heads

Revision ID: 036
Revises: 035
Create Date: 2025-07-07 17:46:07.410196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036'
down_revision ='035'
branch_labels = None
depends_on = None


def upgrade():
    # 1) Tabelas
    op.create_table(
        'Mercante',
        sa.Column('id_mercante', sa.Integer, primary_key=True),
        sa.Column('nome', sa.Text, nullable=False),
    )
    op.create_table(
        'Inventario_Mercante',
        sa.Column('id_mercante', sa.Integer, sa.ForeignKey('Mercante.id_mercante', ondelete='CASCADE'), nullable=False),
        sa.Column('id_item', sa.Integer, sa.ForeignKey('Item.id_Item'), nullable=False),
        sa.Column('preco_venda', sa.Integer, nullable=False),
        sa.Column('preco_compra', sa.Integer, nullable=False),
        sa.Column('quantidade', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('id_mercante', 'id_item'),
    )

    # 2) Procedures
    op.execute("""
    CREATE OR REPLACE PROCEDURE comprar_item(
      p_player INT,
      p_mercante INT,
      p_item INT,
      p_qtde INT
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
      v_preco INT;
      v_custo INT;
      v_espaco INT;
    BEGIN
      SELECT preco_venda, quantidade
        INTO v_preco, v_espaco
      FROM Inventario_Mercante
      WHERE id_mercante = p_mercante
        AND id_item = p_item
      FOR UPDATE;
      IF NOT FOUND OR v_espaco < p_qtde THEN
        RAISE EXCEPTION 'Item % não disponível no mercante % (sobra %)', p_item, p_mercante, v_espaco;
      END IF;
      v_custo := v_preco * p_qtde;
      IF (SELECT gcs FROM Personagem WHERE id_player = p_player) < v_custo THEN
        RAISE EXCEPTION 'Saldo insuficiente: precisa de %, tem %', v_custo, (SELECT gcs FROM Personagem WHERE id_player = p_player);
      END IF;
      SELECT Espaco_Maximo - COALESCE(SUM(Quantidade),0)
        INTO v_espaco
      FROM Inventario_Item
      WHERE Id_PlayerIn = p_player;
      IF v_espaco < p_qtde THEN
        RAISE EXCEPTION 'Espaço insuficiente: só restam %', v_espaco;
      END IF;
      INSERT INTO Inventario_Item (Id_PlayerIn, Id_Item, Quantidade)
        VALUES (p_player, p_item, p_qtde)
      ON CONFLICT (Id_PlayerIn, Id_Item)
        DO UPDATE SET Quantidade = Inventario_Item.Quantidade + EXCLUDED.Quantidade;
      UPDATE Personagem
        SET gcs = gcs - v_custo
        WHERE id_player = p_player;
      UPDATE Inventario_Mercante
        SET quantidade = quantidade - p_qtde
        WHERE id_mercante = p_mercante
          AND id_item = p_item;
    END;
    $$;
    """)

    op.execute("""
    CREATE OR REPLACE PROCEDURE vender_item(
      p_player INT,
      p_mercante INT,
      p_item INT,
      p_qtde INT
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
      v_preco INT;
      v_jogada INT;
    BEGIN
      SELECT Quantidade
        INTO v_jogada
      FROM Inventario_Item
      WHERE Id_PlayerIn = p_player
        AND Id_Item = p_item
      FOR UPDATE;
      IF NOT FOUND OR v_jogada < p_qtde THEN
        RAISE EXCEPTION 'Jogador não possui % do item %', p_qtde, p_item;
      END IF;
      SELECT preco_compra
        INTO v_preco
      FROM Inventario_Mercante
      WHERE id_mercante = p_mercante
        AND id_item = p_item
      FOR UPDATE;
      IF NOT FOUND THEN
        RAISE EXCEPTION 'Mercante % não compra item %', p_mercante, p_item;
      END IF;
      UPDATE Inventario_Item
        SET Quantidade = Quantidade - p_qtde
        WHERE Id_PlayerIn = p_player
          AND Id_Item = p_item;
      DELETE FROM Inventario_Item
        WHERE Id_PlayerIn = p_player
          AND Id_Item = p_item
          AND Quantidade = 0;
      UPDATE Personagem
        SET gcs = gcs + (v_preco * p_qtde)
        WHERE id_player = p_player;
      INSERT INTO Inventario_Mercante (id_mercante, id_item, preco_venda, preco_compra, quantidade)
        VALUES (p_mercante, p_item, (v_preco * 120) / 100, v_preco, p_qtde)
      ON CONFLICT (id_mercante, id_item)
        DO UPDATE SET quantidade = Inventario_Mercante.quantidade + EXCLUDED.quantidade;
    END;
    $$;
    """)

    # 3) Trigger function + trigger
    op.execute("""
    CREATE OR REPLACE FUNCTION trg_check_inventario_mercante()
      RETURNS TRIGGER AS $$
    BEGIN
      IF NEW.quantidade < 0 THEN
        RAISE EXCEPTION 'Quantidade em Inventario_Mercante não pode ser negativa: %', NEW.quantidade;
      END IF;
      IF NEW.preco_venda < NEW.preco_compra THEN
        RAISE EXCEPTION 'Preco_venda (%) deve ser maior ou igual a preco_compra (%).', NEW.preco_venda, NEW.preco_compra;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("DROP TRIGGER IF EXISTS trg_check_inventario_mercante ON Inventario_Mercante;")
    op.execute("""
    CREATE TRIGGER trg_check_inventario_mercante
      BEFORE INSERT OR UPDATE ON Inventario_Mercante
      FOR EACH ROW
      EXECUTE FUNCTION trg_check_inventario_mercante();
    """)


def downgrade():
    # 1) Remover trigger e função
    op.execute("DROP TRIGGER IF EXISTS trg_check_inventario_mercante ON Inventario_Mercante;")
    op.execute("DROP FUNCTION IF EXISTS trg_check_inventario_mercante();")
    # 2) Remover procedures
    op.execute("DROP PROCEDURE IF EXISTS vender_item(INT, INT, INT, INT);")
    op.execute("DROP PROCEDURE IF EXISTS comprar_item(INT, INT, INT, INT);")
    # 3) Remover tabelas
    op.drop_table('Inventario_Mercante')
    op.drop_table('Mercante')