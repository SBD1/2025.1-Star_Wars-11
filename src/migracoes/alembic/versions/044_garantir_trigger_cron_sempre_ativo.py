"""Garantir que o trigger do cron sempre seja ativado quando mob morre

Revision ID: 044
Revises: 043
Create Date: 2025-07-08

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '044'
down_revision = '043'
branch_labels = None
depends_on = None

def upgrade():
    # Modificar a função finalizar_combate para sempre ativar o cron
    op.execute("""
        CREATE OR REPLACE FUNCTION finalizar_combate(p_combate_id INT, p_vencedor VARCHAR(10))
        RETURNS TEXT AS $$
        DECLARE
            v_jogador_id INT;
            v_inimigo_id INT;
            v_jogador_level_atual INT;
            v_novo_level INT;
            v_xp_recompensa INT;
            v_gcs_recompensa INT;
            v_nivel_inimigo INT;
            v_creditos_inimigo INT;
            v_resultado_texto TEXT;
            v_data_inicio_combate TIMESTAMP;
            v_duracao INTERVAL;
            v_total_turnos INT;
            v_dano_total_jogador INT;
            v_dano_total_inimigo INT;
            v_vida_ressurreicao INT;
            v_gcs_atual INT;
            v_xp_atual INT;
            v_loot_texto TEXT := '';
            loot_drop RECORD;
            drop_chance NUMERIC;
            chance_roll NUMERIC;
            v_status_final VARCHAR(20);
            item_nome VARCHAR(50);
        BEGIN
            -- Obter dados do combate
            SELECT id_player, id_mob, data_inicio INTO v_jogador_id, v_inimigo_id, v_data_inicio_combate
            FROM Combate WHERE id_combate = p_combate_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Combate não encontrado';
            END IF;

            -- Determinar status final correto baseado no vencedor
            CASE p_vencedor
                WHEN 'jogador' THEN
                    v_status_final := 'finalizado';
                WHEN 'inimigo' THEN
                    v_status_final := 'finalizado';
                WHEN 'fuga' THEN
                    v_status_final := 'fugiu';
                ELSE
                    v_status_final := 'finalizado';
            END CASE;

            -- Obter dados do inimigo e jogador
            SELECT nivel, creditos INTO v_nivel_inimigo, v_creditos_inimigo
            FROM Inimigo WHERE id_mob = v_inimigo_id;

            SELECT level, gcs, xp INTO v_jogador_level_atual, v_gcs_atual, v_xp_atual
            FROM Personagem WHERE id_player = v_jogador_id;

            -- Calcular estatísticas do combate
            SELECT 
                CURRENT_TIMESTAMP - v_data_inicio_combate,
                COALESCE(MAX(turno_numero), 0),
                COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
            INTO v_duracao, v_total_turnos, v_dano_total_jogador, v_dano_total_inimigo
            FROM Combate_Log WHERE id_combate = p_combate_id;

            -- Processar recompensas se jogador venceu
            IF p_vencedor = 'jogador' THEN
                -- Calcular XP (baseado no nível do inimigo)
                v_xp_recompensa := v_nivel_inimigo * 10;
                
                -- Calcular GCS usando a nova função de drop variável
                v_gcs_recompensa := calcular_drop_creditos(v_inimigo_id);

                -- Atualizar jogador com recompensas
                UPDATE Personagem 
                SET xp = xp + v_xp_recompensa,
                    gcs = gcs + v_gcs_recompensa
                WHERE id_player = v_jogador_id;

                -- Verificar level up
                v_novo_level := FLOOR((v_xp_atual + v_xp_recompensa) / 100) + 1;
                
                IF v_novo_level > v_jogador_level_atual THEN
                    UPDATE Personagem 
                    SET level = v_novo_level,
                        vida_base = vida_base + 10,
                        vida_atual = vida_base + 10,
                        dano_base = dano_base + 2
                    WHERE id_player = v_jogador_id;
                END IF;

                -- Processar loot de itens (usando estrutura correta da Inventario_IA)
                FOR loot_drop IN 
                    SELECT ia.id_item, ia.quantidade, ia.drop_rarity, i.nome
                    FROM Inventario_IA ia
                    JOIN Item i ON ia.id_item = i.id_item
                    WHERE ia.id_mob = v_inimigo_id
                LOOP
                    -- Calcular chance de drop baseada na raridade
                    drop_chance := CASE loot_drop.drop_rarity
                        WHEN 'Comum' THEN 0.6
                        WHEN 'Incomum' THEN 0.25
                        WHEN 'Raro' THEN 0.05
                        WHEN 'Épico' THEN 0.01
                        WHEN 'Garantido' THEN 1.0
                        ELSE 0.5
                    END;

                    chance_roll := random();
                    
                    IF chance_roll <= drop_chance THEN
                        -- Adicionar item ao inventário do jogador usando a função existente
                        PERFORM adicionar_item_inventario(v_jogador_id, loot_drop.id_item, loot_drop.quantidade);
                        
                        v_loot_texto := v_loot_texto || loot_drop.nome || ' x' || loot_drop.quantidade || ', ';
                    END IF;
                END LOOP;

                -- Remover vírgula final do loot
                IF LENGTH(v_loot_texto) > 0 THEN
                    v_loot_texto := RTRIM(v_loot_texto, ', ');
                END IF;

                v_resultado_texto := 'Vitória! Você ganhou ' || v_xp_recompensa || ' XP e ' || v_gcs_recompensa || ' GCS.';
                
                IF v_novo_level > v_jogador_level_atual THEN
                    v_resultado_texto := v_resultado_texto || ' LEVEL UP! Agora você é nível ' || v_novo_level || '!';
                END IF;
                
                IF LENGTH(v_loot_texto) > 0 THEN
                    v_resultado_texto := v_resultado_texto || ' Itens obtidos: ' || v_loot_texto;
                END IF;

            ELSIF p_vencedor = 'inimigo' THEN
                -- Jogador foi derrotado - aplicar penalidades
                v_vida_ressurreicao := GREATEST(FLOOR(v_gcs_atual * 0.1), 10);
                
                UPDATE Personagem 
                SET vida_atual = v_vida_ressurreicao,
                    gcs = GREATEST(gcs - FLOOR(gcs * 0.1), 0)
                WHERE id_player = v_jogador_id;

                v_resultado_texto := 'Derrota! Você perdeu 10% dos seus créditos e foi ressuscitado com ' || v_vida_ressurreicao || ' HP.';
                
            ELSE
                v_resultado_texto := 'Você fugiu do combate.';
            END IF;

            -- Finalizar combate com status correto
            UPDATE Combate
            SET status_combate = v_status_final,
                data_fim = CURRENT_TIMESTAMP
            WHERE id_combate = p_combate_id;

            -- SEMPRE inserir/atualizar resultado do combate para garantir trigger
            INSERT INTO Combate_Resultado (
                id_combate, vencedor, xp_ganho, gcs_ganho, 
                itens_dropados, duracao_combate, total_turnos,
                dano_total_jogador, dano_total_inimigo
            ) VALUES (
                p_combate_id, p_vencedor, COALESCE(v_xp_recompensa, 0), COALESCE(v_gcs_recompensa, 0),
                v_loot_texto, v_duracao, v_total_turnos,
                v_dano_total_jogador, v_dano_total_inimigo
            ) 
            ON CONFLICT (id_combate) 
            DO UPDATE SET 
                vencedor = EXCLUDED.vencedor,
                xp_ganho = EXCLUDED.xp_ganho,
                gcs_ganho = EXCLUDED.gcs_ganho,
                itens_dropados = EXCLUDED.itens_dropados;

            -- FORÇAR execução do cron se jogador venceu (ativar respawn)
            IF p_vencedor = 'jogador' THEN
                PERFORM executar_sistema_cron();
            END IF;

            RETURN v_resultado_texto;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Criar função adicional para ativar cron manualmente no jogo Python
    op.execute("""
        CREATE OR REPLACE FUNCTION ativar_respawn_pos_combate(p_combate_id INT)
        RETURNS TEXT AS $$
        DECLARE
            v_inimigo_id INT;
            inimigo_setor_id INT;
        BEGIN
            -- Obter o id_mob do combate
            SELECT id_mob INTO v_inimigo_id
            FROM Combate 
            WHERE id_combate = p_combate_id;
            
            IF v_inimigo_id IS NOT NULL THEN
                -- Encontrar o inimigo_setor correspondente
                SELECT ies.id_inimigo_setor INTO inimigo_setor_id
                FROM Inimigo_Setor ies
                WHERE ies.id_mob = v_inimigo_id
                LIMIT 1;
                
                -- Reduzir quantidade atual se encontrado
                IF inimigo_setor_id IS NOT NULL THEN
                    UPDATE Mob_Respawn_Control 
                    SET quantidade_atual = GREATEST(quantidade_atual - 1, 0)
                    WHERE id_inimigo_setor = inimigo_setor_id;
                    
                    -- Executar cron para processar respawn
                    PERFORM executar_sistema_cron();
                    
                    RETURN 'Respawn ativado para combate ' || p_combate_id;
                END IF;
            END IF;
            
            RETURN 'Nenhum respawn necessário';
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover função adicional
    op.execute("DROP FUNCTION IF EXISTS ativar_respawn_pos_combate(INT);")
