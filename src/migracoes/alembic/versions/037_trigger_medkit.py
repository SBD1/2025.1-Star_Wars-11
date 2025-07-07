"""trigger medkit

Revision ID: 037
Revises: 036
Create Date: 2025-07-07 20:12:16.278960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '037'
down_revision = '036'
branch_labels = None
depends_on = None


def upgrade():
    print("Iniciando aprimoramento do sistema de itens...")

    # --- Bloco 1: Corrigir o dado do "Kit Médico" existente ---
    print("Passo 1/3: Corrigindo 'Kit Médico' existente...")
    op.execute("""
        UPDATE Item
        SET
            efeito_tipo = 'CURA_VIDA',
            efeito_valor = 50
        WHERE nome = 'Kit Médico';
    """)

    # --- Bloco 2: Adicionar o gatilho de itens iniciais para novos personagens ---
    print("Passo 2/3: Criando gatilho para itens iniciais...")
    op.execute("""
        -- A FUNÇÃO que o gatilho vai executar
        CREATE OR REPLACE FUNCTION adicionar_kits_medicos_iniciais()
        RETURNS TRIGGER AS $$
        DECLARE
            v_kit_medico_id INT;
            v_inventario_id INT;
        BEGIN
            SELECT id_item INTO v_kit_medico_id FROM Item WHERE nome = 'Kit Médico' LIMIT 1;
            IF NOT FOUND THEN RETURN NEW; END IF;

            SELECT Id_PlayerIn INTO v_inventario_id FROM Inventario WHERE Id_Player = NEW.id_player;
            IF NOT FOUND THEN RETURN NEW; END IF;

            PERFORM adicionar_item_inventario(NEW.id_player, v_kit_medico_id, 2);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        -- O TRIGGER que se conecta à tabela Personagem
        CREATE TRIGGER trigger_adicionar_itens_iniciais
            AFTER INSERT ON Personagem
            FOR EACH ROW
            EXECUTE FUNCTION adicionar_kits_medicos_iniciais();
    """)

    # --- Bloco 3: Atualizar a função de usar item com a validação de vida cheia ---
    print("Passo 3/3: Atualizando função 'usar_item_inventario'...")
    op.execute("""
        CREATE OR REPLACE FUNCTION usar_item_inventario(p_jogador_id INT, p_item_id INT)
        RETURNS TEXT AS $$
        DECLARE
            v_inventario_id INT;
            v_item_info RECORD;
            v_personagem_info RECORD;
            v_quantidade_atual INT;
        BEGIN
            SELECT Id_PlayerIn INTO v_inventario_id FROM Inventario WHERE Id_Player = p_jogador_id;
            SELECT quantidade INTO v_quantidade_atual FROM Inventario_Item WHERE Id_PlayerIn = v_inventario_id AND id_item = p_item_id;
            IF NOT FOUND OR v_quantidade_atual <= 0 THEN
                RAISE EXCEPTION 'Você não possui o item com ID %.', p_item_id;
            END IF;

            SELECT * INTO v_item_info FROM Item WHERE id_item = p_item_id;
            IF v_item_info.efeito_tipo IS NULL THEN
                RAISE EXCEPTION 'O item "%" não pode ser usado.', v_item_info.nome;
            END IF;

            CASE v_item_info.efeito_tipo
                WHEN 'CURA_VIDA' THEN
                    SELECT vida_atual, vida_base INTO v_personagem_info FROM Personagem WHERE id_player = p_jogador_id;
                    IF v_personagem_info.vida_atual >= v_personagem_info.vida_base THEN
                        RAISE EXCEPTION 'Sua vida já está cheia. Você não pode usar este item agora.';
                    END IF;
                    UPDATE Personagem SET vida_atual = LEAST(v_personagem_info.vida_base, vida_atual + v_item_info.efeito_valor) WHERE id_player = p_jogador_id;
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
    """)
    print("Sistema de itens aprimorado com sucesso!")


def downgrade():
    print("Revertendo aprimoramento do sistema de itens...")

    # --- Reverter Bloco 3: Retornar a função 'usar_item_inventario' à versão anterior ---
    print("Passo 1/3: Revertendo função 'usar_item_inventario'...")
    op.execute("""
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
    """)

    # --- Reverter Bloco 2: Remover o gatilho ---
    print("Passo 2/3: Removendo gatilho de itens iniciais...")
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_adicionar_itens_iniciais ON Personagem;
        DROP FUNCTION IF EXISTS adicionar_kits_medicos_iniciais();
    """)

    # --- Reverter Bloco 1: Desfazer a correção do item ---
    print("Passo 3/3: Revertendo dados do 'Kit Médico'...")
    op.execute("""
        UPDATE Item
        SET
            efeito_tipo = NULL,
            efeito_valor = NULL
        WHERE nome = 'Kit Médico';
    """)
    print("Reversão concluída.")
