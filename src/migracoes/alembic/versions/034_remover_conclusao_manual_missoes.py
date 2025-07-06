"""Remover conclusão manual de missões - apenas por trigger

Revision ID: 034
Revises: 033
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '034'
down_revision = '033'
branch_labels = None
depends_on = None

def upgrade():
    # Criar função para listar missões de boss ativas (apenas informativo)
    op.execute("""
        CREATE OR REPLACE FUNCTION listar_missoes_boss_ativas(jogador_id INT)
        RETURNS TABLE (
            id_missao_boss INT,
            nome_missao VARCHAR(100),
            descricao TEXT,
            tipo_mob_alvo VARCHAR(22),
            recompensa_xp INT,
            recompensa_gcs INT,
            data_aceitacao TIMESTAMP,
            status_missao VARCHAR(20)
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                mb.id_missao_boss,
                mb.nome_missao,
                mb.descricao,
                mb.tipo_mob_alvo,
                mb.recompensa_xp,
                mb.recompensa_gcs,
                pmb.data_aceitacao,
                pmb.status_missao
            FROM Personagem_Missao_Boss pmb
            JOIN Missao_Boss mb ON pmb.id_missao_boss = mb.id_missao_boss
            WHERE pmb.id_player = jogador_id
            ORDER BY 
                CASE pmb.status_missao
                    WHEN 'ativa' THEN 1
                    WHEN 'concluida' THEN 2
                    ELSE 3
                END,
                pmb.data_aceitacao DESC;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Criar função para abandonar missão de boss (se necessário)
    op.execute("""
        CREATE OR REPLACE FUNCTION abandonar_missao_boss(jogador_id INT, missao_id INT)
        RETURNS TEXT AS $$
        DECLARE
            missao_status VARCHAR(20);
        BEGIN
            -- Verificar se a missão existe e está ativa
            SELECT pmb.status_missao
            INTO missao_status
            FROM Personagem_Missao_Boss pmb
            WHERE pmb.id_player = jogador_id 
              AND pmb.id_missao_boss = missao_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Voce nao possui esta missao.';
            END IF;
            
            IF missao_status = 'concluida' THEN
                RETURN 'Erro: Nao e possivel abandonar uma missao ja concluida.';
            END IF;
            
            -- Remover a missão
            DELETE FROM Personagem_Missao_Boss
            WHERE id_player = jogador_id AND id_missao_boss = missao_id;
            
            RETURN 'Missao abandonada com sucesso.';
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Melhorar o trigger para dar feedback mais detalhado
    op.execute("""
        DROP FUNCTION IF EXISTS trigger_missao_boss_concluida() CASCADE;
        CREATE OR REPLACE FUNCTION trigger_missao_boss_concluida()
        RETURNS TRIGGER AS $$
        DECLARE
            boss_tipo VARCHAR(22);
            jogador_id INT;
            missoes_concluidas INT := 0;
            recompensa_total_xp INT := 0;
            recompensa_total_gcs INT := 0;
        BEGIN
            -- Verificar se o resultado é vitória do jogador
            IF NEW.vencedor = 'jogador' THEN
                -- Obter tipo do boss morto e jogador
                SELECT i.tipo_mob, c.id_player
                INTO boss_tipo, jogador_id
                FROM Combate c
                JOIN Inimigo i ON c.id_mob = i.id_mob
                WHERE c.id_combate = NEW.id_combate;
                
                -- Verificar se é um boss (existe na tabela Boss)
                IF EXISTS (SELECT 1 FROM Boss WHERE tipo_mob = boss_tipo) THEN
                    -- Calcular recompensas das missões que serão completadas
                    SELECT COUNT(*), COALESCE(SUM(mb.recompensa_xp), 0), COALESCE(SUM(mb.recompensa_gcs), 0)
                    INTO missoes_concluidas, recompensa_total_xp, recompensa_total_gcs
                    FROM Personagem_Missao_Boss pmb
                    JOIN Missao_Boss mb ON pmb.id_missao_boss = mb.id_missao_boss
                    WHERE pmb.id_player = jogador_id
                      AND pmb.status_missao = 'ativa'
                      AND mb.tipo_mob_alvo = boss_tipo;
                    
                    -- Se há missões para completar
                    IF missoes_concluidas > 0 THEN
                        -- Completar missões ativas relacionadas a este boss
                        UPDATE Personagem_Missao_Boss pmb
                        SET status_missao = 'concluida',
                            data_conclusao = CURRENT_TIMESTAMP
                        FROM Missao_Boss mb
                        WHERE pmb.id_missao_boss = mb.id_missao_boss
                          AND pmb.id_player = jogador_id
                          AND pmb.status_missao = 'ativa'
                          AND mb.tipo_mob_alvo = boss_tipo;
                        
                        -- Dar recompensas das missões completadas
                        UPDATE Personagem
                        SET xp = xp + recompensa_total_xp,
                            gcs = gcs + recompensa_total_gcs
                        WHERE id_player = jogador_id;
                        
                        -- Log da conclusão (opcional - para debug)
                        INSERT INTO Combate_Log (id_combate, turno, ator, acao, dano_causado, vida_restante, observacoes)
                        VALUES (NEW.id_combate, 999, 'sistema', 'missao_concluida', 0, 0, 
                               'Missoes de boss concluidas: ' || missoes_concluidas || 
                               '. Recompensas: ' || recompensa_total_xp || ' XP, ' || recompensa_total_gcs || ' GCS');
                    END IF;
                END IF;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Recriar o trigger
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_boss_missao_concluida ON Combate_Resultado;
        CREATE TRIGGER trigger_boss_missao_concluida
        AFTER INSERT ON Combate_Resultado
        FOR EACH ROW
        EXECUTE FUNCTION trigger_missao_boss_concluida();
    """)

def downgrade():
    # Remover funções criadas
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_boss_missao_concluida ON Combate_Resultado;
        DROP FUNCTION IF EXISTS trigger_missao_boss_concluida();
        DROP FUNCTION IF EXISTS abandonar_missao_boss(INT, INT);
        DROP FUNCTION IF EXISTS listar_missoes_boss_ativas(INT);
    """)
    
    # Recriar trigger simples
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_missao_boss_concluida()
        RETURNS TRIGGER AS $$
        DECLARE
            boss_tipo VARCHAR(22);
            jogador_id INT;
        BEGIN
            IF NEW.vencedor = 'jogador' THEN
                SELECT i.tipo_mob, c.id_player
                INTO boss_tipo, jogador_id
                FROM Combate c
                JOIN Inimigo i ON c.id_mob = i.id_mob
                WHERE c.id_combate = NEW.id_combate;
                
                IF EXISTS (SELECT 1 FROM Boss WHERE tipo_mob = boss_tipo) THEN
                    UPDATE Personagem_Missao_Boss pmb
                    SET status_missao = 'concluida',
                        data_conclusao = CURRENT_TIMESTAMP
                    FROM Missao_Boss mb
                    WHERE pmb.id_missao_boss = mb.id_missao_boss
                      AND pmb.id_player = jogador_id
                      AND pmb.status_missao = 'ativa'
                      AND mb.tipo_mob_alvo = boss_tipo;
                END IF;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER trigger_boss_missao_concluida
        AFTER INSERT ON Combate_Resultado
        FOR EACH ROW
        EXECUTE FUNCTION trigger_missao_boss_concluida();
    """)
