"""Corrigir missões de boss para usar setores reais

Revision ID: 033
Revises: 032
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '033'
down_revision = '032'
branch_labels = None
depends_on = None

def upgrade():
    # Limpar missões antigas com setores fictícios
    op.execute("DELETE FROM Missao_Boss;")
    
    # Inserir missões com setores reais que existem no banco
    op.execute("""
        INSERT INTO Missao_Boss (nome_missao, descricao, tipo_mob_alvo, planeta_origem, setor_aceitacao, recompensa_xp, recompensa_gcs, nivel_minimo) VALUES
        
        -- Missão do Rancor (Tatooine) - usar setor real
        ('Eliminar o Rancor das Cavernas', 
         'Um Rancor gigante está aterrorizando os moradores locais. Elimine esta criatura perigosa.',
         'Rancor', 'Tatooine', 'Mos Eisley', 500, 1000, 8),
        
        -- Missão do Krayt Dragon (Tatooine) - usar setor real
        ('Cacar o Dragao Krayt Lendario', 
         'O lendario Dragao Krayt foi avistado no deserto. Esta e uma missao extremamente perigosa.',
         'Krayt_Dragon', 'Tatooine', 'Deserto de Jundland', 1500, 3000, 15),
        
        -- Missão do Sith Lord (Coruscant) - usar setor real
        ('Confrontar o Lorde Sith', 
         'Um poderoso Lorde Sith foi detectado nas areas urbanas. Derrote-o antes que cause mais destruicao.',
         'Sith_Lord', 'Coruscant', 'Nivel 1313', 1000, 2000, 12),
        
        -- Missão do AT-ST (Coruscant) - usar setor real
        ('Destruir o AT-ST Imperial', 
         'Um AT-ST Imperial esta patrulhando a regiao. Destrua este veiculo de combate.',
         'AT_ST', 'Coruscant', 'Templo Jedi', 800, 1500, 10);
    """)
    
    # Atualizar função para verificar setor corretamente
    op.execute("""
        DROP FUNCTION IF EXISTS aceitar_missao_boss(INT, INT);
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
                RETURN 'Erro: Missao nao encontrada ou inativa.';
            END IF;
            
            -- Verificar se já aceitou a missão
            SELECT EXISTS(
                SELECT 1 FROM Personagem_Missao_Boss 
                WHERE id_player = jogador_id AND id_missao_boss = missao_id
            ) INTO ja_aceita;
            
            IF ja_aceita THEN
                RETURN 'Voce ja aceitou esta missao.';
            END IF;
            
            -- Verificar nível
            IF jogador_level < nivel_minimo THEN
                RETURN 'Nivel insuficiente. Nivel minimo: ' || nivel_minimo;
            END IF;
            
            -- Verificar planeta
            IF jogador_planeta != missao_planeta THEN
                RETURN 'Voce deve estar no planeta ' || missao_planeta || ' para aceitar esta missao.';
            END IF;
            
            -- Verificar setor
            IF jogador_setor != missao_setor THEN
                RETURN 'Voce deve estar no setor "' || missao_setor || '" para aceitar esta missao.';
            END IF;
            
            -- Aceitar missão
            INSERT INTO Personagem_Missao_Boss (id_player, id_missao_boss, status_missao)
            VALUES (jogador_id, missao_id, 'ativa');
            
            RETURN 'Missao aceita com sucesso!';
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para missões antigas
    op.execute("DELETE FROM Missao_Boss;")
    
    op.execute("""
        INSERT INTO Missao_Boss (nome_missao, descricao, tipo_mob_alvo, planeta_origem, setor_aceitacao, recompensa_xp, recompensa_gcs, nivel_minimo) VALUES
        
        -- Missões antigas com setores fictícios
        ('Eliminar o Rancor das Cavernas', 
         'Um Rancor gigante está aterrorizando os moradores locais. Elimine esta criatura perigosa.',
         'Rancor', 'Tatooine', 'Cantina de Chalmun', 500, 1000, 8),
        
        ('Confrontar o Lorde Sith', 
         'Um poderoso Lorde Sith foi detectado nas florestas sombrias. Derrote-o antes que cause mais destruição.',
         'Sith_Lord', 'Kashyyyk', 'Posto Avancado', 1000, 2000, 12),
        
        ('Destruir o AT-ST Imperial', 
         'Um AT-ST Imperial está patrulhando a região. Destrua este veículo de combate.',
         'AT_ST', 'Hoth', 'Base Rebelde', 800, 1500, 10),
        
        ('Caçar o Dragão Krayt Lendário', 
         'O lendário Dragão Krayt foi avistado no deserto. Esta é uma missão extremamente perigosa.',
         'Krayt_Dragon', 'Tatooine', 'Porto Espacial', 1500, 3000, 15);
    """)
