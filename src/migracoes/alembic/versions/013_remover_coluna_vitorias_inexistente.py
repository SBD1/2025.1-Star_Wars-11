"""Remover referência à coluna vitorias inexistente na função finalizar_combate

Revision ID: 013
Revises: 012
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '013'
down_revision = '012'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir a função finalizar_combate removendo referência à coluna vitorias
    op.execute("""
        -- Remover função existente
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        
        -- Recriar função sem referência à coluna vitorias
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

            -- Calcular duracao
            duracao := CURRENT_TIMESTAMP - data_inicio_combate;

            -- Obter estatisticas do combate
            SELECT COUNT(*),
                   COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
                   COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
            INTO total_turnos, dano_total_jogador, dano_total_inimigo
            FROM Combate_Log WHERE id_combate = combate_id;

            -- Obter dados do inimigo para recompensas
            SELECT nivel, creditos INTO nivel_inimigo, creditos_inimigo
            FROM Inimigo WHERE id_mob = inimigo_id;

            -- Obter level atual do jogador
            SELECT level INTO jogador_level_atual FROM Personagem WHERE id_player = jogador_id;

            IF vencedor = 'jogador' THEN
                -- Calcular recompensas baseadas no nivel do inimigo
                xp_recompensa := (nivel_inimigo * 15) + 10;
                gcs_recompensa := creditos_inimigo + (nivel_inimigo * 5);
                
                -- Calcular novo level (cada 100 XP = 1 level)
                novo_level := jogador_level_atual;
                IF (SELECT xp FROM Personagem WHERE id_player = jogador_id) + xp_recompensa >= (jogador_level_atual * 100) THEN
                    novo_level := jogador_level_atual + 1;
                END IF;

                -- Atualizar jogador com recompensas (SEM coluna vitorias)
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vida_base = 100  -- Restaurar vida apos vitoria
                WHERE id_player = jogador_id;

                resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

            ELSIF vencedor = 'inimigo' THEN
                -- Jogador foi derrotado
                SELECT gcs INTO gcs_atual FROM Personagem WHERE id_player = jogador_id;
                
                IF gcs_atual >= 50 THEN
                    -- Tem dinheiro para pagar penalidade
                    vida_ressurreicao := 100;
                    UPDATE Personagem 
                    SET gcs = gcs - 50, 
                        vida_base = vida_ressurreicao,
                        mortes = mortes + 1
                    WHERE id_player = jogador_id;
                    resultado_texto := 'Voce foi derrotado! Perdeu 50 GCS mas foi ressuscitado com vida completa.';
                ELSE
                    -- Nao tem dinheiro suficiente
                    vida_ressurreicao := 50;
                    UPDATE Personagem 
                    SET gcs = 0, 
                        vida_base = vida_ressurreicao,
                        mortes = mortes + 1
                    WHERE id_player = jogador_id;
                    resultado_texto := 'Voce foi derrotado! Nao tinha GCS suficiente. Ressuscitado com 50 de vida.';
                END IF;

            ELSE
                -- Fuga
                resultado_texto := 'Voce fugiu do combate!';
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
    # Reverter para a versão anterior (com problema da coluna vitorias)
    op.execute("""
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        
        -- Recriar função com problema da coluna vitorias
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

            -- Calcular duracao
            duracao := CURRENT_TIMESTAMP - data_inicio_combate;

            -- Obter estatisticas do combate
            SELECT COUNT(*),
                   COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
                   COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
            INTO total_turnos, dano_total_jogador, dano_total_inimigo
            FROM Combate_Log WHERE id_combate = combate_id;

            -- Obter dados do inimigo para recompensas
            SELECT nivel, creditos INTO nivel_inimigo, creditos_inimigo
            FROM Inimigo WHERE id_mob = inimigo_id;

            -- Obter level atual do jogador
            SELECT level INTO jogador_level_atual FROM Personagem WHERE id_player = jogador_id;

            IF vencedor = 'jogador' THEN
                -- Calcular recompensas baseadas no nivel do inimigo
                xp_recompensa := (nivel_inimigo * 15) + 10;
                gcs_recompensa := creditos_inimigo + (nivel_inimigo * 5);
                
                -- Calcular novo level (cada 100 XP = 1 level)
                novo_level := jogador_level_atual;
                IF (SELECT xp FROM Personagem WHERE id_player = jogador_id) + xp_recompensa >= (jogador_level_atual * 100) THEN
                    novo_level := jogador_level_atual + 1;
                END IF;

                -- Atualizar jogador com recompensas (COM problema da coluna vitorias)
                UPDATE Personagem
                SET xp = xp + xp_recompensa,
                    gcs = gcs + gcs_recompensa,
                    level = novo_level,
                    vitorias = vitorias + 1,  -- PROBLEMA: coluna não existe
                    vida_base = 100  -- Restaurar vida apos vitoria
                WHERE id_player = jogador_id;

                resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

            ELSIF vencedor = 'inimigo' THEN
                -- Jogador foi derrotado
                SELECT gcs INTO gcs_atual FROM Personagem WHERE id_player = jogador_id;
                
                IF gcs_atual >= 50 THEN
                    -- Tem dinheiro para pagar penalidade
                    vida_ressurreicao := 100;
                    UPDATE Personagem 
                    SET gcs = gcs - 50, 
                        vida_base = vida_ressurreicao,
                        mortes = mortes + 1
                    WHERE id_player = jogador_id;
                    resultado_texto := 'Voce foi derrotado! Perdeu 50 GCS mas foi ressuscitado com vida completa.';
                ELSE
                    -- Nao tem dinheiro suficiente
                    vida_ressurreicao := 50;
                    UPDATE Personagem 
                    SET gcs = 0, 
                        vida_base = vida_ressurreicao,
                        mortes = mortes + 1
                    WHERE id_player = jogador_id;
                    resultado_texto := 'Voce foi derrotado! Nao tinha GCS suficiente. Ressuscitado com 50 de vida.';
                END IF;

            ELSE
                -- Fuga
                resultado_texto := 'Voce fugiu do combate!';
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
