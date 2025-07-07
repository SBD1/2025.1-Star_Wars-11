"""inventario e loot

Revision ID: 035
Revises: 034
Create Date: 2025-07-07 19:08:34.620764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '035'
down_revision = '034'
branch_labels = None
depends_on = None


def upgrade():
    # Bloco 1: Alterações na tabela Item (sem modificações)
    op.execute("""
        ALTER TABLE Item
        ADD COLUMN IF NOT EXISTS efeito_tipo VARCHAR(20),
        ADD COLUMN IF NOT EXISTS efeito_valor INT;

        COMMENT ON COLUMN Item.efeito_tipo IS 'Define a ação que o item executa (ex: CURA_VIDA).';
        COMMENT ON COLUMN Item.efeito_valor IS 'O valor numérico do efeito (ex: 50 para curar 50 de vida).';

        -- Atualiza o Medkit para ter um efeito de cura (ajuste o ID se for diferente)
        UPDATE Item 
        SET efeito_tipo = 'CURA_VIDA', efeito_valor = 50
        WHERE nome = 'Medkit'; -- Mais seguro usar o nome
    """)

    # Bloco 2: Refatoração da tabela Inventario_IA (COM A CORREÇÃO)
    print("Refatorando a tabela Inventario_IA para usar IDs de item...")
    op.execute("""
        -- Adicionar as novas colunas
        ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS id_item INT;
        ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS drop_rarity VARCHAR(20);
        SELECT setval(
            pg_get_serial_sequence('Item', 'id_item'),
            COALESCE((SELECT MAX(id_item) FROM Item), 0) + 1,
            false
        );

        -- Inserir itens que existem em Inventario_IA mas não em Item
        WITH unique_items_from_ia AS (
            SELECT DISTINCT item AS nome_item FROM Inventario_IA WHERE item IS NOT NULL
        )
        INSERT INTO Item (nome, Peso, tipo, preco)
        SELECT 
            ui.nome_item, 1, 'Recurso', 10
        FROM unique_items_from_ia ui
        LEFT JOIN Item i ON ui.nome_item = i.nome
        WHERE i.id_item IS NULL;
        
        -- Preencher a nova coluna 'id_item' em Inventario_IA
        UPDATE Inventario_IA ia SET id_item = i.id_item FROM Item i WHERE ia.item = i.nome;
        
        -- Copiar dados da coluna 'raridade' para a nova 'drop_rarity'
        UPDATE Inventario_IA SET drop_rarity = raridade WHERE raridade IS NOT NULL;
        
        -- Tornar a coluna id_item obrigatória (NOT NULL)
        ALTER TABLE Inventario_IA ALTER COLUMN id_item SET NOT NULL;
        
        -- Remover colunas antigas
        ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS item;
        ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS raridade;
        
        -- Adicionar a chave estrangeira
        ALTER TABLE Inventario_IA DROP CONSTRAINT IF EXISTS inventario_ia_id_item_fkey;
        ALTER TABLE Inventario_IA ADD CONSTRAINT inventario_ia_id_item_fkey
            FOREIGN KEY (id_item) REFERENCES Item(id_item) ON DELETE CASCADE;
    """)

    # Bloco 3: Criação e atualização de Funções (COM A CORREÇÃO)
    print("Criando e atualizando funções de inventário e combate...")
    op.execute("""
    DROP FUNCTION IF EXISTS adicionar_item_inventario(INT, INT, INT);
    DROP FUNCTION IF EXISTS usar_item_inventario(INT, INT);
    DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));

    -- Agora, recriamos as funções com a nova lógica
    CREATE OR REPLACE FUNCTION adicionar_item_inventario(p_jogador_id INT, p_item_id INT, p_quantidade INT)
    RETURNS TEXT AS $$
    DECLARE
        inventario_id INT;
    BEGIN
        SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = p_jogador_id;
        IF NOT FOUND THEN RAISE EXCEPTION 'Inventário para o jogador ID % não encontrado.', p_jogador_id; END IF;
        
        INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade)
        VALUES (inventario_id, p_item_id, p_quantidade)
        ON CONFLICT (Id_PlayerIn, id_item)
        DO UPDATE SET quantidade = Inventario_Item.quantidade + EXCLUDED.quantidade;
        
        RETURN (SELECT nome FROM Item WHERE id_item = p_item_id) || ' (x' || p_quantidade || ') adicionado ao inventário.';
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION usar_item_inventario(p_jogador_id INT, p_item_id INT)
    RETURNS TEXT AS $$
    DECLARE
        inventario_id INT;
        item_info RECORD;
        quantidade_atual INT;
        vida_maxima INT;
    BEGIN
        SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = p_jogador_id;
        SELECT quantidade INTO quantidade_atual FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = p_item_id;
        IF NOT FOUND OR quantidade_atual <= 0 THEN RAISE EXCEPTION 'Você não possui o item com ID %.', p_item_id; END IF;

        SELECT nome, efeito_tipo, efeito_valor INTO item_info FROM Item WHERE id_item = p_item_id;
        IF item_info.efeito_tipo IS NULL THEN RAISE EXCEPTION 'O item "%" não pode ser usado.', item_info.nome; END IF;

        CASE item_info.efeito_tipo
            WHEN 'CURA_VIDA' THEN
                SELECT vida_base INTO vida_maxima FROM Personagem WHERE id_player = p_jogador_id;
                UPDATE Personagem SET vida_atual = LEAST(vida_maxima, vida_atual + item_info.efeito_valor) WHERE id_player = p_jogador_id;
            ELSE
                RAISE EXCEPTION 'Tipo de efeito desconhecido: %', item_info.efeito_tipo;
        END CASE;

        IF quantidade_atual > 1 THEN
            UPDATE Inventario_Item SET quantidade = quantidade - 1 WHERE Id_PlayerIn = inventario_id AND id_item = p_item_id;
        ELSE
            DELETE FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = p_item_id;
        END IF;
        
        RETURN 'Você usou ' || item_info.nome || '. Sua vida foi restaurada!';
    END;
    $$ LANGUAGE plpgsql;

    CREATE OR REPLACE FUNCTION finalizar_combate(p_combate_id INT, p_vencedor VARCHAR(10))
    RETURNS TEXT AS $$
    DECLARE
        v_jogador_id INT;
        v_inimigo_id INT;
        v_resultado_texto TEXT;
        v_loot_texto TEXT := '';
        v_xp_recompensa INT;
        v_gcs_recompensa INT;
        loot_drop RECORD;
        drop_chance NUMERIC;
        chance_roll NUMERIC;
    BEGIN
        SELECT id_player, id_mob INTO v_jogador_id, v_inimigo_id FROM Combate WHERE id_combate = p_combate_id;
        IF NOT FOUND THEN RAISE EXCEPTION 'Combate ID % não encontrado.', p_combate_id; END IF;

        IF p_vencedor = 'jogador' THEN
            -- Lógica de recompensa
            SELECT (nivel * 50 + 25), creditos INTO v_xp_recompensa, v_gcs_recompensa FROM Inimigo WHERE id_mob = v_inimigo_id;
            UPDATE Personagem SET xp = xp + v_xp_recompensa, gcs = gcs + v_gcs_recompensa WHERE id_player = v_jogador_id;
            v_resultado_texto := 'Vitoria! Voce ganhou ' || v_xp_recompensa || ' XP e ' || v_gcs_recompensa || ' GCS.';

            -- Lógica de Loot
            FOR loot_drop IN SELECT * FROM Inventario_IA WHERE id_mob = v_inimigo_id LOOP
                drop_chance := CASE loot_drop.drop_rarity
                                    WHEN 'Comum' THEN 60.0 WHEN 'Incomum' THEN 25.0 WHEN 'Raro' THEN 5.0
                                    WHEN 'Épico' THEN 1.0 WHEN 'Garantido' THEN 100.0 ELSE 0.0
                                END;
                chance_roll := random() * 100;
                IF chance_roll < drop_chance THEN
                    PERFORM adicionar_item_inventario(v_jogador_id, loot_drop.id_item, loot_drop.quantidade);
                    v_loot_texto := v_loot_texto || ' | Loot: ' || (SELECT nome FROM Item WHERE id_item = loot_drop.id_item) || ' (x' || loot_drop.quantidade || ')';
                END IF;
            END LOOP;
            v_resultado_texto := v_resultado_texto || v_loot_texto;

        ELSIF p_vencedor = 'inimigo' THEN
            -- Lógica de penalidade
            UPDATE Personagem SET mortes = mortes + 1, gcs = GREATEST(gcs - 100, 0), vida_atual = 50 WHERE id_player = v_jogador_id;
            v_resultado_texto := 'Derrota! Você foi derrotado e perdeu alguns GCS.';
        ELSE
            v_resultado_texto := 'Voce fugiu do combate.';
        END IF;

        UPDATE Combate SET status_combate = p_vencedor, data_fim = CURRENT_TIMESTAMP WHERE id_combate = p_combate_id;
        RETURN v_resultado_texto;
    END;
    $$ LANGUAGE plpgsql;
""")


def downgrade():
    # A função downgrade desfaz o que o upgrade fez, na ordem inversa
    print("Revertendo: Removendo funções de inventário e combate...")
    op.execute("DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));")
    op.execute("DROP FUNCTION IF EXISTS usar_item_inventario(INT, INT);")
    op.execute("DROP FUNCTION IF EXISTS adicionar_item_inventario(INT, INT, INT);")

    print("Revertendo: Refatoração da tabela Inventario_IA...")
    op.execute("""
        ALTER TABLE Inventario_IA DROP CONSTRAINT IF EXISTS inventario_ia_id_item_fkey;
        ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS item VARCHAR(50);
        ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS raridade VARCHAR(20);
        
        -- (Opcional) Tentar repopular os dados. Pode ser complexo e ter perdas.
        -- UPDATE Inventario_IA ia SET item = i.nome, raridade = ia.drop_rarity FROM Item i WHERE ia.id_item = i.id_item;
        
        ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS id_item;
        ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS drop_rarity;
    """)

    print("Revertendo: Alterações na tabela Item...")
    op.execute("""
        ALTER TABLE Item
        DROP COLUMN IF EXISTS efeito_tipo,
        DROP COLUMN IF EXISTS efeito_valor;
    """)
