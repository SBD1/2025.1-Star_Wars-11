"""inventario e loot upgrade

Revision ID: 036
Revises: 035
Create Date: 2025-07-07 19:28:23.445879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '036'
down_revision = '035'
branch_labels = None
depends_on = None


def upgrade():
    # Bloco 1: Refatoração da tabela Inventario_IA para usar IDs de item
    print("Passo 1/1: Criando e atualizando as funções de inventário...")
    op.execute("""
        -- Primeiro, removemos as funções se existirem para garantir a recriação limpa
        DROP FUNCTION IF EXISTS administrar_adicionar_item(INT, TEXT, INT);
        DROP FUNCTION IF EXISTS usar_item_inventario(INT, INT);
        DROP FUNCTION IF EXISTS listar_inventario_jogador(INT);
        DROP FUNCTION IF EXISTS adicionar_item_inventario(INT, INT, INT);

        -- Agora, criamos as novas versões
        CREATE OR REPLACE FUNCTION adicionar_item_inventario(p_jogador_id INT, p_item_id INT, p_quantidade INT)
        RETURNS TEXT AS $$
        DECLARE
            v_inventario_id INT;
        BEGIN
            SELECT Id_PlayerIn INTO v_inventario_id FROM Inventario WHERE Id_Player = p_jogador_id;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Inventário para o jogador ID % não encontrado.', p_jogador_id;
            END IF;

            INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade)
            VALUES (v_inventario_id, p_item_id, p_quantidade)
            ON CONFLICT (Id_PlayerIn, id_item)
            DO UPDATE SET quantidade = Inventario_Item.quantidade + EXCLUDED.quantidade;

            RETURN (SELECT nome FROM Item WHERE id_item = p_item_id) || ' (x' || p_quantidade || ') adicionado ao inventário.';
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION listar_inventario_jogador(p_jogador_id INT)
        RETURNS TABLE (id_item INT, nome_item VARCHAR(50), quantidade INT, tipo_item VARCHAR(20), peso_item INT) AS $$
        BEGIN
            RETURN QUERY
            SELECT i.id_item, i.nome, ii.quantidade, i.tipo, i.Peso
            FROM Inventario inv
            JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
            JOIN Item i ON ii.id_item = i.id_item
            WHERE inv.Id_Player = p_jogador_id
            ORDER BY i.nome;
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION usar_item_inventario(p_jogador_id INT, p_item_id INT)
        RETURNS TEXT AS $$
        DECLARE
            v_inventario_id INT;
            v_item_info RECORD;
            v_quantidade_atual INT;
            v_vida_maxima INT;
        BEGIN
            SELECT Id_PlayerIn INTO v_inventario_id FROM Inventario WHERE Id_Player = p_jogador_id;
            SELECT quantidade INTO v_quantidade_atual FROM Inventario_Item WHERE Id_PlayerIn = v_inventario_id AND id_item = p_item_id;

            IF NOT FOUND OR v_quantidade_atual <= 0 THEN
                RAISE EXCEPTION 'Você não possui o item com ID %.', p_item_id;
            END IF;

            SELECT nome, efeito_tipo, efeito_valor INTO v_item_info FROM Item WHERE id_item = p_item_id;
            IF v_item_info.efeito_tipo IS NULL THEN
                RAISE EXCEPTION 'O item "%" não pode ser usado.', v_item_info.nome;
            END IF;

            CASE v_item_info.efeito_tipo
                WHEN 'CURA_VIDA' THEN
                    SELECT vida_base INTO v_vida_maxima FROM Personagem WHERE id_player = p_jogador_id;
                    UPDATE Personagem SET vida_atual = LEAST(v_vida_maxima, vida_atual + v_item_info.efeito_valor) WHERE id_player = p_jogador_id;
                ELSE
                    RAISE EXCEPTION 'Tipo de efeito desconhecido: %', v_item_info.efeito_tipo;
            END CASE;

            IF v_quantidade_atual > 1 THEN
                UPDATE Inventario_Item SET quantidade = quantidade - 1 WHERE Id_PlayerIn = v_inventario_id AND id_item = p_item_id;
            ELSE
                DELETE FROM Inventario_Item WHERE Id_PlayerIn = v_inventario_id AND id_item = p_item_id;
            END IF;

            RETURN 'Você usou ' || v_item_info.nome || '. Sua vida foi restaurada!';
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION administrar_adicionar_item(p_player_id INT, p_item_name TEXT, p_quantity INT)
        RETURNS TEXT AS $$
        DECLARE
            v_item_id INT;
        BEGIN
            SELECT id_item INTO v_item_id FROM Item WHERE nome = p_item_name;
            IF NOT FOUND THEN
                RAISE EXCEPTION 'Item com o nome "%" não foi encontrado.', p_item_name;
            END IF;
            RETURN adicionar_item_inventario(p_player_id, v_item_id, p_quantity);
        END;
        $$ LANGUAGE plpgsql;
    """)
    print("Fim da migração.")


def downgrade():
    print("Iniciando reversão da migração...")

    # A função downgrade agora desfaz apenas o que a nova função upgrade faz.
    print("Revertendo: Removendo funções de inventário...")
    op.execute("""
        DROP FUNCTION IF EXISTS administrar_adicionar_item(INT, TEXT, INT);
        DROP FUNCTION IF EXISTS usar_item_inventario(INT, INT);
        DROP FUNCTION IF EXISTS listar_inventario_jogador(INT);
        DROP FUNCTION IF EXISTS adicionar_item_inventario(INT, INT, INT);
    """)

    # A parte que revertia a tabela Inventario_IA foi removida,
    # pois isso agora é responsabilidade da migração 035.
    print("Fim da reversão.")