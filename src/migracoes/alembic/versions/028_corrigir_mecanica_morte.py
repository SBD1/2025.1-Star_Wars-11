"""Corrigir mecânica de morte para usar vida_atual em vez de vida_base

Revision ID: 028
Revises: 027
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '028'
down_revision = '027'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir função finalizar_combate para usar vida_atual
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

                -- Atualizar jogador com recompensas e restaurar vida completa
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vida_atual = vida_base  -- Restaurar vida completa após vitória
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
                -- Fuga - apenas restaurar vida completa
                UPDATE Personagem
                SET vida_atual = vida_base
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
    # Reverter para versão anterior que usava vida_base
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
                IF (SELECT xp FROM Personagem WHERE id_player = jogador_id) + xp_recompensa >= (jogador_level_atual * 100) THEN
                    novo_level := jogador_level_atual + 1;
                END IF;

                -- Atualizar jogador com recompensas
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vida_base = 100  -- Restaurar vida apos vitoria (PROBLEMA: usa vida_base)
                WHERE id_player = jogador_id;

                resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

                IF novo_level > jogador_level_atual THEN
                    resultado_texto := resultado_texto || ' Parabens! Voce subiu para o level ' || novo_level || '!';
                END IF;

            ELSIF vencedor = 'inimigo' THEN
                -- Jogador foi derrotado
                SELECT level, gcs INTO jogador_level_atual, gcs_atual FROM Personagem WHERE id_player = jogador_id;

                -- Determinar vida de ressurreicao baseada nos GCS
                IF gcs_atual >= 100 THEN
                    vida_ressurreicao := 100;  -- Vida completa se tiver dinheiro
                ELSE
                    vida_ressurreicao := 50;   -- Vida reduzida se nao tiver dinheiro
                END IF;

                -- Aplicar penalidades por morte
                UPDATE Personagem
                SET mortes = mortes + 1,
                    gcs = GREATEST(gcs - 100, 0),  -- Perde 100 GCS (minimo 0)
                    xp = GREATEST(xp - (jogador_level_atual * 10), 0),  -- Perde XP baseado no level
                    vida_base = vida_ressurreicao  -- Vida baseada nos GCS disponiveis (PROBLEMA: usa vida_base)
                WHERE id_player = jogador_id;

                -- Mensagem personalizada baseada na situacao
                IF gcs_atual >= 100 THEN
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.';
                ELSE
                    resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).';
                END IF;
            ELSE
                -- Fuga - apenas restaurar vida
                UPDATE Personagem
                SET vida_base = 100  -- PROBLEMA: usa vida_base
                WHERE id_player = jogador_id;

                resultado_texto := 'Voce fugiu do combate.';
            END IF;

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
