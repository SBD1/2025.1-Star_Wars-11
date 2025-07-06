"""Corrigir vida após vitória - não curar automaticamente

Revision ID: 029
Revises: 028
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '029'
down_revision = '028'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir função finalizar_combate para não curar automaticamente após vitória
    op.execute("""
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        CREATE OR REPLACE FUNCTION finalizar_combate(combate_id INT, vencedor VARCHAR(10))
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            jogador_level_atual INT;
            novo_level INT;
            xp_recompensa INT;
            gcs_recompensa INT;
            nivel_inimigo INT;
            creditos_inimigo INT;
            resultado_texto TEXT;
            data_inicio_combate TIMESTAMP;
            duracao INTERVAL;
            total_turnos INT;
            dano_total_jogador INT;
            dano_total_inimigo INT;
            vida_ressurreicao INT;
            gcs_atual INT;
            xp_atual INT;
            vida_atual_combate INT;
        BEGIN
            -- Obter dados do combate
            SELECT id_player, id_mob, data_inicio, vida_jogador_atual 
            INTO jogador_id, inimigo_id, data_inicio_combate, vida_atual_combate
            FROM Combate WHERE id_combate = combate_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Combate nao encontrado';
            END IF;

            -- Calcular estatísticas do combate
            duracao := CURRENT_TIMESTAMP - data_inicio_combate;
            
            SELECT COUNT(*) INTO total_turnos
            FROM Combate_Log WHERE id_combate = combate_id;
            
            SELECT COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
                   COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
            INTO dano_total_jogador, dano_total_inimigo
            FROM Combate_Log WHERE id_combate = combate_id;

            IF vencedor = 'jogador' THEN
                -- Jogador venceu
                SELECT level, nivel, creditos INTO jogador_level_atual, nivel_inimigo, creditos_inimigo
                FROM Personagem p, Inimigo i
                WHERE p.id_player = jogador_id AND i.id_mob = inimigo_id;

                -- Calcular recompensas baseadas no nivel do inimigo
                xp_recompensa := (nivel_inimigo * 15) + 10;
                gcs_recompensa := creditos_inimigo + (nivel_inimigo * 5);
                
                -- Calcular novo level (cada 100 XP = 1 level)
                novo_level := jogador_level_atual;
                SELECT xp INTO xp_atual FROM Personagem WHERE id_player = jogador_id;
                IF xp_atual + xp_recompensa >= (jogador_level_atual * 100) THEN
                    novo_level := jogador_level_atual + 1;
                END IF;

                -- Atualizar jogador com recompensas MANTENDO a vida atual do combate
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vida_atual = vida_atual_combate  -- Manter vida atual do final do combate
                WHERE id_player = jogador_id;

                resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

                IF novo_level > jogador_level_atual THEN
                    resultado_texto := resultado_texto || ' Parabens! Voce subiu para o level ' || novo_level || '!';
                END IF;

            ELSIF vencedor = 'inimigo' THEN
                -- Jogador foi derrotado - aplicar mecânica de morte
                SELECT level, gcs, xp INTO jogador_level_atual, gcs_atual, xp_atual 
                FROM Personagem WHERE id_player = jogador_id;

                -- Determinar vida de ressurreição baseada nos GCS (penalidade: 100 GCS)
                IF gcs_atual >= 100 THEN
                    -- Tem dinheiro para pagar penalidade completa
                    vida_ressurreicao := 100;  -- Vida completa
                    UPDATE Personagem
                    SET mortes = mortes + 1,
                        gcs = gcs - 100,  -- Perde 100 GCS
                        xp = GREATEST(xp - (jogador_level_atual * 10), 0),  -- Perde XP baseado no level
                        vida_atual = vida_ressurreicao  -- Ressuscita com vida completa
                    WHERE id_player = jogador_id;
                    
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.';
                ELSE
                    -- Não tem dinheiro suficiente - ressuscita com vida reduzida
                    vida_ressurreicao := 50;   -- Vida reduzida (50% da vida base)
                    UPDATE Personagem
                    SET mortes = mortes + 1,
                        gcs = 0,  -- Perde todos os GCS restantes
                        xp = GREATEST(xp - (jogador_level_atual * 10), 0),  -- Perde XP baseado no level
                        vida_atual = vida_ressurreicao  -- Ressuscita com vida reduzida
                    WHERE id_player = jogador_id;
                    
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).';
                END IF;

            ELSE
                -- Fuga - manter vida atual do combate
                UPDATE Personagem
                SET vida_atual = vida_atual_combate
                WHERE id_player = jogador_id;

                resultado_texto := 'Voce fugiu do combate.';
            END IF;

            -- Registrar resultado do combate
            INSERT INTO Combate_Resultado (
                id_combate, vencedor, xp_ganho, gcs_ganho, 
                duracao_combate, total_turnos, dano_total_jogador, dano_total_inimigo
            ) VALUES (
                combate_id, vencedor, COALESCE(xp_recompensa, 0), COALESCE(gcs_recompensa, 0),
                duracao, total_turnos, dano_total_jogador, dano_total_inimigo
            );

            -- Finalizar combate
            UPDATE Combate
            SET status_combate = CASE
                                    WHEN vencedor = 'jogador' THEN 'vitoria'
                                    WHEN vencedor = 'inimigo' THEN 'derrota'
                                    ELSE 'fugiu'
                                END,
                data_fim = CURRENT_TIMESTAMP
            WHERE id_combate = combate_id;

            RETURN resultado_texto;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para versão que curava automaticamente após vitória
    op.execute("""
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        CREATE OR REPLACE FUNCTION finalizar_combate(combate_id INT, vencedor VARCHAR(10))
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            jogador_level_atual INT;
            novo_level INT;
            xp_recompensa INT;
            gcs_recompensa INT;
            nivel_inimigo INT;
            creditos_inimigo INT;
            resultado_texto TEXT;
            data_inicio_combate TIMESTAMP;
            duracao INTERVAL;
            total_turnos INT;
            dano_total_jogador INT;
            dano_total_inimigo INT;
            vida_ressurreicao INT;
            gcs_atual INT;
            xp_atual INT;
        BEGIN
            -- Obter dados do combate
            SELECT id_player, id_mob, data_inicio INTO jogador_id, inimigo_id, data_inicio_combate
            FROM Combate WHERE id_combate = combate_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Combate nao encontrado';
            END IF;

            -- Calcular estatísticas do combate
            duracao := CURRENT_TIMESTAMP - data_inicio_combate;
            
            SELECT COUNT(*) INTO total_turnos
            FROM Combate_Log WHERE id_combate = combate_id;
            
            SELECT COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
                   COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
            INTO dano_total_jogador, dano_total_inimigo
            FROM Combate_Log WHERE id_combate = combate_id;

            IF vencedor = 'jogador' THEN
                -- Jogador venceu
                SELECT level, nivel, creditos INTO jogador_level_atual, nivel_inimigo, creditos_inimigo
                FROM Personagem p, Inimigo i
                WHERE p.id_player = jogador_id AND i.id_mob = inimigo_id;

                -- Calcular recompensas baseadas no nivel do inimigo
                xp_recompensa := (nivel_inimigo * 15) + 10;
                gcs_recompensa := creditos_inimigo + (nivel_inimigo * 5);
                
                -- Calcular novo level (cada 100 XP = 1 level)
                novo_level := jogador_level_atual;
                SELECT xp INTO xp_atual FROM Personagem WHERE id_player = jogador_id;
                IF xp_atual + xp_recompensa >= (jogador_level_atual * 100) THEN
                    novo_level := jogador_level_atual + 1;
                END IF;

                -- Atualizar jogador com recompensas e restaurar vida completa (PROBLEMA)
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vida_atual = vida_base  -- Restaurar vida completa após vitória (PROBLEMA)
                WHERE id_player = jogador_id;

                resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

                IF novo_level > jogador_level_atual THEN
                    resultado_texto := resultado_texto || ' Parabens! Voce subiu para o level ' || novo_level || '!';
                END IF;

            ELSIF vencedor = 'inimigo' THEN
                -- Jogador foi derrotado - aplicar mecânica de morte
                SELECT level, gcs, xp INTO jogador_level_atual, gcs_atual, xp_atual 
                FROM Personagem WHERE id_player = jogador_id;

                -- Determinar vida de ressurreição baseada nos GCS (penalidade: 100 GCS)
                IF gcs_atual >= 100 THEN
                    -- Tem dinheiro para pagar penalidade completa
                    vida_ressurreicao := 100;  -- Vida completa
                    UPDATE Personagem
                    SET mortes = mortes + 1,
                        gcs = gcs - 100,  -- Perde 100 GCS
                        xp = GREATEST(xp - (jogador_level_atual * 10), 0),  -- Perde XP baseado no level
                        vida_atual = vida_ressurreicao  -- Ressuscita com vida completa
                    WHERE id_player = jogador_id;
                    
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.';
                ELSE
                    -- Não tem dinheiro suficiente - ressuscita com vida reduzida
                    vida_ressurreicao := 50;   -- Vida reduzida (50% da vida base)
                    UPDATE Personagem
                    SET mortes = mortes + 1,
                        gcs = 0,  -- Perde todos os GCS restantes
                        xp = GREATEST(xp - (jogador_level_atual * 10), 0),  -- Perde XP baseado no level
                        vida_atual = vida_ressurreicao  -- Ressuscita com vida reduzida
                    WHERE id_player = jogador_id;
                    
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).';
                END IF;

            ELSE
                -- Fuga - apenas restaurar vida completa (PROBLEMA)
                UPDATE Personagem
                SET vida_atual = vida_base  -- PROBLEMA: restaura vida completa
                WHERE id_player = jogador_id;

                resultado_texto := 'Voce fugiu do combate.';
            END IF;

            -- Registrar resultado do combate
            INSERT INTO Combate_Resultado (
                id_combate, vencedor, xp_ganho, gcs_ganho, 
                duracao_combate, total_turnos, dano_total_jogador, dano_total_inimigo
            ) VALUES (
                combate_id, vencedor, COALESCE(xp_recompensa, 0), COALESCE(gcs_recompensa, 0),
                duracao, total_turnos, dano_total_jogador, dano_total_inimigo
            );

            -- Finalizar combate
            UPDATE Combate
            SET status_combate = CASE
                                    WHEN vencedor = 'jogador' THEN 'vitoria'
                                    WHEN vencedor = 'inimigo' THEN 'derrota'
                                    ELSE 'fugiu'
                                END,
                data_fim = CURRENT_TIMESTAMP
            WHERE id_combate = combate_id;

            RETURN resultado_texto;
        END;
        $$ LANGUAGE plpgsql;
    """)
