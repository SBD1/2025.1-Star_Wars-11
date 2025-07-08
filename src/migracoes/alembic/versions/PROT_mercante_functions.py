# src/migracoes/versions/039_add_mercante_functions.py
"""add mercante functions

Revision ID: 039
Revises: 038
Create Date: 2025-07-07 22:30:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'nc823d82j'
down_revision = 'dsjididain'
branch_labels = None
depends_on = None


def upgrade():
    # Função: listar produtos
    op.execute("""
    CREATE OR REPLACE FUNCTION listar_produtos_mercante(p_mercante_id INT)
    RETURNS TABLE (
      id_item   INT,
      nome_item VARCHAR,
      preco     INT,
      estoque   INT
    ) AS $$
    BEGIN
      RETURN QUERY
      SELECT mp.id_item, i.nome, mp.preco, mp.estoque
        FROM Mercante_Produto mp
        JOIN Item i ON i.id_item = mp.id_item
       WHERE mp.id_mercante = p_mercante_id
       ORDER BY i.nome;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Função: comprar
    op.execute("""
    CREATE OR REPLACE FUNCTION mercante_comprar(
      p_player_id   INT,
      p_mercante_id INT,
      p_item_id     INT
    ) RETURNS TEXT AS $$
    DECLARE
      v_preco   INT;
      v_estoque INT;
      v_saldo   INT;
    BEGIN
      SELECT preco, estoque INTO v_preco, v_estoque
        FROM Mercante_Produto
       WHERE id_mercante = p_mercante_id
         AND id_item      = p_item_id;
      IF NOT FOUND OR v_estoque <= 0 THEN
        RAISE EXCEPTION 'Produto indisponível.';
      END IF;

      SELECT gcs INTO v_saldo FROM Personagem WHERE id_player = p_player_id;
      IF v_saldo < v_preco THEN
        RAISE EXCEPTION 'GCS insuficientes.';
      END IF;

      UPDATE Personagem SET gcs = gcs - v_preco WHERE id_player = p_player_id;
      UPDATE Mercante_Produto
         SET estoque = estoque - 1
       WHERE id_mercante = p_mercante_id AND id_item = p_item_id;

      PERFORM adicionar_item_inventario(p_player_id, p_item_id, 1);
      RETURN format(
        'Você comprou 1× % por % GCS.',
        (SELECT nome FROM Item WHERE id_item = p_item_id),
        v_preco
      );
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Função: vender
    op.execute("""
    CREATE OR REPLACE FUNCTION mercante_vender(
      p_player_id   INT,
      p_mercante_id INT,
      p_item_id     INT
    ) RETURNS TEXT AS $$
    DECLARE
      v_qtde INT;
      v_preco INT;
      v_retorno INT;
    BEGIN
      SELECT ii.quantidade INTO v_qtde
        FROM Inventario inv
        JOIN Inventario_Item ii ON ii.Id_PlayerIn = inv.Id_PlayerIn
       WHERE inv.Id_Player = p_player_id
         AND ii.id_item    = p_item_id;
      IF NOT FOUND OR v_qtde <= 0 THEN
        RAISE EXCEPTION 'Você não possui esse item.';
      END IF;

      SELECT preco INTO v_preco
        FROM Mercante_Produto
       WHERE id_mercante = p_mercante_id
         AND id_item      = p_item_id;
      IF NOT FOUND THEN
        RAISE EXCEPTION 'Mercante não negocia este item.';
      END IF;

      v_retorno := v_preco / 2;

      IF v_qtde > 1 THEN
        UPDATE Inventario_Item
           SET quantidade = quantidade - 1
         WHERE id_item = p_item_id
           AND Id_PlayerIn = (SELECT Id_PlayerIn FROM Inventario WHERE Id_Player = p_player_id);
      ELSE
        DELETE FROM Inventario_Item
         WHERE id_item = p_item_id
           AND Id_PlayerIn = (SELECT Id_PlayerIn FROM Inventario WHERE Id_Player = p_player_id);
      END IF;

      UPDATE Personagem SET gcs = gcs + v_retorno WHERE id_player = p_player_id;
      UPDATE Mercante_Produto
         SET estoque = estoque + 1
       WHERE id_mercante = p_mercante_id AND id_item = p_item_id;

      RETURN format(
        'Você vendeu 1× % e recebeu % GCS.',
        (SELECT nome FROM Item WHERE id_item = p_item_id),
        v_retorno
      );
    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS mercante_vender(INT, INT, INT);")
    op.execute("DROP FUNCTION IF EXISTS mercante_comprar(INT, INT, INT);")
    op.execute("DROP FUNCTION IF EXISTS listar_produtos_mercante(INT);")
