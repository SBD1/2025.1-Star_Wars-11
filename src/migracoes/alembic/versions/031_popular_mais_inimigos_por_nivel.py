"""Popular mais inimigos seguindo lógica de nível de perigo

Revision ID: 031
Revises: 030
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '031'
down_revision = '030'
branch_labels = None
depends_on = None

def upgrade():
    # Adicionar novos tipos de MOB
    op.execute("""
        -- Novos MOBs Normal
        INSERT INTO MOB (tipo_mob, nivel_ameaca) VALUES
        ('Battle_Droid', 2),
        ('Jawa', 1),
        ('Tusken_Raider', 3),
        ('Imperial_Guard', 4);

        -- Novos MOBs Elite
        INSERT INTO MOB (tipo_mob, nivel_ameaca) VALUES
        ('Elite_Guard', 6),
        ('Assassin_Droid', 7),
        ('Sith_Apprentice', 8);

        -- Novos MOBs Boss
        INSERT INTO MOB (tipo_mob, nivel_ameaca) VALUES
        ('Sith_Lord', 15),
        ('AT_ST', 12),
        ('Krayt_Dragon', 18);
    """)
    
    # Adicionar novos inimigos Normal
    op.execute("""
        INSERT INTO Inimigo (tipo_mob, vida_base, nivel, dano_base, pontos_escudo, creditos, planeta_origem) VALUES
        -- Normal (aparecem em níveis 1-5)
        ('Battle_Droid', 80, 2, 15, 10, 40, 'Naboo'),
        ('Jawa', 60, 1, 10, 0, 25, 'Tatooine'),
        ('Tusken_Raider', 120, 3, 25, 5, 75, 'Tatooine'),
        ('Imperial_Guard', 150, 4, 30, 20, 100, 'Coruscant');
    """)
    
    # Adicionar novos inimigos Elite
    op.execute("""
        INSERT INTO Inimigo (tipo_mob, vida_base, nivel, dano_base, pontos_escudo, creditos, planeta_origem) VALUES
        -- Elite (aparecem em níveis 3-5)
        ('Elite_Guard', 250, 6, 50, 40, 200, 'Coruscant'),
        ('Assassin_Droid', 220, 5, 45, 30, 180, 'Naboo'),
        ('Sith_Apprentice', 300, 7, 60, 50, 250, 'Kashyyyk');
    """)
    
    # Adicionar novos inimigos Boss
    op.execute("""
        INSERT INTO Inimigo (tipo_mob, vida_base, nivel, dano_base, pontos_escudo, creditos, planeta_origem) VALUES
        -- Boss (aparecem apenas em níveis 4-5)
        ('Sith_Lord', 800, 15, 120, 100, 800, 'Kashyyyk'),
        ('AT_ST', 600, 12, 100, 150, 600, 'Hoth'),
        ('Krayt_Dragon', 1000, 18, 150, 80, 1000, 'Tatooine');
    """)
    
    # Adicionar às tabelas de especialização
    op.execute("""
        -- Novos Normal
        INSERT INTO Normal (tipo_mob, Formacao_Tatica, Patrulha, Ataque_Coordenado) VALUES
        ('Battle_Droid', false, true, true),
        ('Jawa', false, false, false),
        ('Tusken_Raider', true, true, false),
        ('Imperial_Guard', true, true, true);
        
        -- Novos Elite
        INSERT INTO Elite (tipo_mob, Armadura_Reforçada, Ataque_Especial, Regeneracao) VALUES
        ('Elite_Guard', true, true, false),
        ('Assassin_Droid', false, true, true),
        ('Sith_Apprentice', true, true, true);
        
        -- Novos Boss
        INSERT INTO Boss (tipo_mob, Arsenal, Habilidade_Unica, Invocacao_Aliados) VALUES
        ('Sith_Lord', 'Sabre Duplo', true, true),
        ('AT_ST', 'Canhoes Laser', true, false),
        ('Krayt_Dragon', 'Garras Venenosas', true, false);
    """)
    
    # Limpar distribuição atual de inimigos nos setores
    op.execute("DELETE FROM Inimigo_Setor;")
    
    # Distribuir inimigos por nível de perigo
    op.execute("""
        -- NÍVEL 1 (Muito Seguro): Apenas Normal fracos
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        JOIN MOB m ON i.tipo_mob = m.tipo_mob
        WHERE s.nivel_perigo = 1 
          AND i.tipo_mob IN ('Jawa', 'Stormtrooper')
          AND EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = i.tipo_mob);
    """)
    
    op.execute("""
        -- NÍVEL 2 (Seguro): Normal variados
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 2
        FROM Setor s
        CROSS JOIN Inimigo i
        JOIN MOB m ON i.tipo_mob = m.tipo_mob
        WHERE s.nivel_perigo = 2 
          AND i.tipo_mob IN ('Stormtrooper', 'Battle_Droid', 'Jawa')
          AND EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = i.tipo_mob);
    """)
    
    op.execute("""
        -- NÍVEL 3 (Moderado): Normal + Elite
        -- Normal
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 2
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 3 
          AND i.tipo_mob IN ('Stormtrooper', 'Battle_Droid', 'Tusken_Raider', 'Imperial_Guard')
          AND EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = i.tipo_mob);
          
        -- Elite
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 3 
          AND i.tipo_mob IN ('Dark_Trooper', 'Elite_Guard')
          AND EXISTS (SELECT 1 FROM Elite WHERE tipo_mob = i.tipo_mob);
    """)
    
    op.execute("""
        -- NÍVEL 4 (Perigoso): Normal + Elite + Boss
        -- Normal
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 4 
          AND i.tipo_mob IN ('Stormtrooper', 'Tusken_Raider', 'Imperial_Guard')
          AND EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = i.tipo_mob);
          
        -- Elite
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 2
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 4 
          AND i.tipo_mob IN ('Dark_Trooper', 'Elite_Guard', 'Assassin_Droid')
          AND EXISTS (SELECT 1 FROM Elite WHERE tipo_mob = i.tipo_mob);
          
        -- Boss
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 4 
          AND i.tipo_mob IN ('Rancor', 'AT_ST')
          AND EXISTS (SELECT 1 FROM Boss WHERE tipo_mob = i.tipo_mob);
    """)
    
    op.execute("""
        -- NÍVEL 5 (Muito Perigoso): Todos os tipos, incluindo Boss mais fortes
        -- Normal
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 5 
          AND i.tipo_mob IN ('Imperial_Guard', 'Tusken_Raider')
          AND EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = i.tipo_mob);
          
        -- Elite
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 2
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 5 
          AND i.tipo_mob IN ('Dark_Trooper', 'Elite_Guard', 'Assassin_Droid', 'Sith_Apprentice')
          AND EXISTS (SELECT 1 FROM Elite WHERE tipo_mob = i.tipo_mob);
          
        -- Boss
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, i.id_mob, 1
        FROM Setor s
        CROSS JOIN Inimigo i
        WHERE s.nivel_perigo = 5 
          AND i.tipo_mob IN ('Rancor', 'Sith_Lord', 'AT_ST', 'Krayt_Dragon')
          AND EXISTS (SELECT 1 FROM Boss WHERE tipo_mob = i.tipo_mob);
    """)

def downgrade():
    # Remover novos inimigos e MOBs
    op.execute("""
        DELETE FROM Inimigo_Setor;
        DELETE FROM Normal WHERE tipo_mob IN ('Battle_Droid', 'Jawa', 'Tusken_Raider', 'Imperial_Guard');
        DELETE FROM Elite WHERE tipo_mob IN ('Elite_Guard', 'Assassin_Droid', 'Sith_Apprentice');
        DELETE FROM Boss WHERE tipo_mob IN ('Sith_Lord', 'AT_ST', 'Krayt_Dragon');
        DELETE FROM Inimigo WHERE tipo_mob IN ('Battle_Droid', 'Jawa', 'Tusken_Raider', 'Imperial_Guard', 'Elite_Guard', 'Assassin_Droid', 'Sith_Apprentice', 'Sith_Lord', 'AT_ST', 'Krayt_Dragon');
        DELETE FROM MOB WHERE tipo_mob IN ('Battle_Droid', 'Jawa', 'Tusken_Raider', 'Imperial_Guard', 'Elite_Guard', 'Assassin_Droid', 'Sith_Apprentice', 'Sith_Lord', 'AT_ST', 'Krayt_Dragon');
    """)
