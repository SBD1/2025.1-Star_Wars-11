"""Sistema de missões de boss com triggers automáticos

Revision ID: 032
Revises: 031
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '032'
down_revision = '031'
branch_labels = None
depends_on = None

def upgrade():
    # Criar tabela de missões de boss
    op.execute("""
        CREATE TABLE IF NOT EXISTS Missao_Boss (
            id_missao_boss INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            nome_missao VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL,
            tipo_mob_alvo VARCHAR(22) NOT NULL, -- Tipo do boss que deve ser morto
            planeta_origem VARCHAR(20) NOT NULL, -- Planeta onde a missão está disponível
            setor_aceitacao VARCHAR(50) NOT NULL, -- Setor específico para aceitar
            recompensa_xp INT DEFAULT 0,
            recompensa_gcs INT DEFAULT 0,
            nivel_minimo INT DEFAULT 1,
            ativa BOOLEAN DEFAULT true,
            FOREIGN KEY (tipo_mob_alvo) REFERENCES MOB(tipo_mob),
            FOREIGN KEY (planeta_origem) REFERENCES Planeta(nome_planeta)
        );
    """)
    
    # Criar tabela de missões aceitas pelos jogadores
    op.execute("""
        CREATE TABLE IF NOT EXISTS Personagem_Missao_Boss (
            id_personagem_missao INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            id_player INT NOT NULL,
            id_missao_boss INT NOT NULL,
            status_missao VARCHAR(20) DEFAULT 'ativa', -- ativa, concluida, falhada
            data_aceitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_conclusao TIMESTAMP NULL,
            FOREIGN KEY (id_player) REFERENCES Personagem(id_player) ON DELETE CASCADE,
            FOREIGN KEY (id_missao_boss) REFERENCES Missao_Boss(id_missao_boss) ON DELETE CASCADE,
            UNIQUE(id_player, id_missao_boss)
        );
    """)
    
    # Popular missões de boss
    op.execute("""
        INSERT INTO Missao_Boss (nome_missao, descricao, tipo_mob_alvo, planeta_origem, setor_aceitacao, recompensa_xp, recompensa_gcs, nivel_minimo) VALUES
        
        -- Missão do Rancor (Tatooine)
        ('Eliminar o Rancor das Cavernas', 
         'Um Rancor gigante está aterrorizando os moradores locais. Elimine esta criatura perigosa.',
         'Rancor', 'Tatooine', 'Cantina de Chalmun', 500, 1000, 8),
        
        -- Missão do Sith Lord (Kashyyyk)
        ('Confrontar o Lorde Sith', 
         'Um poderoso Lorde Sith foi detectado nas florestas sombrias. Derrote-o antes que cause mais destruição.',
         'Sith_Lord', 'Kashyyyk', 'Posto Avancado', 1000, 2000, 12),
        
        -- Missão do AT-ST (Hoth)
        ('Destruir o AT-ST Imperial', 
         'Um AT-ST Imperial está patrulhando a região. Destrua este veículo de combate.',
         'AT_ST', 'Hoth', 'Base Rebelde', 800, 1500, 10),
        
        -- Missão do Krayt Dragon (Tatooine)
        ('Caçar o Dragão Krayt Lendário', 
         'O lendário Dragão Krayt foi avistado no deserto. Esta é uma missão extremamente perigosa.',
         'Krayt_Dragon', 'Tatooine', 'Porto Espacial', 1500, 3000, 15);
    """)
    
    # Criar função para verificar missões disponíveis por planeta
    op.execute("""
        CREATE OR REPLACE FUNCTION listar_missoes_boss_planeta(jogador_id INT)
        RETURNS TABLE (
            id_missao_boss INT,
            nome_missao VARCHAR(100),
            descricao TEXT,
            tipo_mob_alvo VARCHAR(22),
            setor_aceitacao VARCHAR(50),
            recompensa_xp INT,
            recompensa_gcs INT,
            nivel_minimo INT,
            pode_aceitar BOOLEAN,
            ja_aceita BOOLEAN,
            status_atual VARCHAR(20)
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                mb.id_missao_boss,
                mb.nome_missao,
                mb.descricao,
                mb.tipo_mob_alvo,
                mb.setor_aceitacao,
                mb.recompensa_xp,
                mb.recompensa_gcs,
                mb.nivel_minimo,
                (p.level >= mb.nivel_minimo) AS pode_aceitar,
                (pmb.id_personagem_missao IS NOT NULL) AS ja_aceita,
                COALESCE(pmb.status_missao, 'nao_aceita') AS status_atual
            FROM Missao_Boss mb
            JOIN Personagem p ON p.nome_planeta = mb.planeta_origem
            LEFT JOIN Personagem_Missao_Boss pmb ON pmb.id_player = p.id_player 
                                                 AND pmb.id_missao_boss = mb.id_missao_boss
            WHERE p.id_player = jogador_id 
              AND mb.ativa = true
            ORDER BY mb.nivel_minimo, mb.nome_missao;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Criar função para aceitar missão (só no setor correto)
    op.execute("""
        CREATE OR REPLACE FUNCTION aceitar_missao_boss(jogador_id INT, missao_id INT)
        RETURNS TEXT AS $$
        DECLARE
            jogador_planeta VARCHAR(20);
            jogador_setor VARCHAR(50);
            missao_planeta VARCHAR(20);
            missao_setor VARCHAR(50);
            jogador_level INT;
            nivel_minimo INT;
            ja_aceita BOOLEAN;
        BEGIN
            -- Obter dados do jogador
            SELECT p.nome_planeta, s.nome_setor, p.level
            INTO jogador_planeta, jogador_setor, jogador_level
            FROM Personagem p
            LEFT JOIN Setor s ON p.id_setor = s.id_setor
            WHERE p.id_player = jogador_id;
            
            -- Obter dados da missão
            SELECT mb.planeta_origem, mb.setor_aceitacao, mb.nivel_minimo
            INTO missao_planeta, missao_setor, nivel_minimo
            FROM Missao_Boss mb
            WHERE mb.id_missao_boss = missao_id AND mb.ativa = true;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Missão não encontrada ou inativa.';
            END IF;
            
            -- Verificar se já aceitou a missão
            SELECT EXISTS(
                SELECT 1 FROM Personagem_Missao_Boss 
                WHERE id_player = jogador_id AND id_missao_boss = missao_id
            ) INTO ja_aceita;
            
            IF ja_aceita THEN
                RETURN 'Você já aceitou esta missão.';
            END IF;
            
            -- Verificar nível
            IF jogador_level < nivel_minimo THEN
                RETURN 'Nível insuficiente. Nível mínimo: ' || nivel_minimo;
            END IF;
            
            -- Verificar planeta
            IF jogador_planeta != missao_planeta THEN
                RETURN 'Você deve estar no planeta ' || missao_planeta || ' para aceitar esta missão.';
            END IF;
            
            -- Verificar setor
            IF jogador_setor != missao_setor THEN
                RETURN 'Você deve estar no setor "' || missao_setor || '" para aceitar esta missão.';
            END IF;
            
            -- Aceitar missão
            INSERT INTO Personagem_Missao_Boss (id_player, id_missao_boss, status_missao)
            VALUES (jogador_id, missao_id, 'ativa');
            
            RETURN 'Missão aceita com sucesso!';
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Criar trigger para detectar morte de boss e completar missões
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_missao_boss_concluida()
        RETURNS TRIGGER AS $$
        DECLARE
            boss_tipo VARCHAR(22);
            jogador_id INT;
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
                    SET xp = xp + (
                        SELECT COALESCE(SUM(mb.recompensa_xp), 0)
                        FROM Personagem_Missao_Boss pmb
                        JOIN Missao_Boss mb ON pmb.id_missao_boss = mb.id_missao_boss
                        WHERE pmb.id_player = jogador_id
                          AND pmb.status_missao = 'concluida'
                          AND pmb.data_conclusao = CURRENT_TIMESTAMP
                          AND mb.tipo_mob_alvo = boss_tipo
                    ),
                    gcs = gcs + (
                        SELECT COALESCE(SUM(mb.recompensa_gcs), 0)
                        FROM Personagem_Missao_Boss pmb
                        JOIN Missao_Boss mb ON pmb.id_missao_boss = mb.id_missao_boss
                        WHERE pmb.id_player = jogador_id
                          AND pmb.status_missao = 'concluida'
                          AND pmb.data_conclusao = CURRENT_TIMESTAMP
                          AND mb.tipo_mob_alvo = boss_tipo
                    )
                    WHERE id_player = jogador_id;
                END IF;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Criar o trigger
    op.execute("""
        CREATE TRIGGER trigger_boss_missao_concluida
        AFTER INSERT ON Combate_Resultado
        FOR EACH ROW
        EXECUTE FUNCTION trigger_missao_boss_concluida();
    """)

def downgrade():
    # Remover trigger e função
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_boss_missao_concluida ON Combate_Resultado;
        DROP FUNCTION IF EXISTS trigger_missao_boss_concluida();
        DROP FUNCTION IF EXISTS aceitar_missao_boss(INT, INT);
        DROP FUNCTION IF EXISTS listar_missoes_boss_planeta(INT);
        DROP TABLE IF EXISTS Personagem_Missao_Boss CASCADE;
        DROP TABLE IF EXISTS Missao_Boss CASCADE;
    """)
