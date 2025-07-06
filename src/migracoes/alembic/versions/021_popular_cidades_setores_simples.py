"""Popular mais cidades e setores para todos os planetas - versão simplificada

Revision ID: 021
Revises: 020
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '021'
down_revision = '020'
branch_labels = None
depends_on = None

def upgrade():
    # Executar o script de expansão de cidades e setores (versão simplificada)
    op.execute("""
        -- TATOOINE - Adicionar mais cidades
        INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
        ('Anchorhead', 'Tatooine', 'Pequena cidade de mineracao no deserto'),
        ('Bestine', 'Tatooine', 'Capital administrativa de Tatooine')
        ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

        -- CORUSCANT - Adicionar mais cidades
        INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
        ('Distrito Senatorial', 'Coruscant', 'Area residencial dos senadores'),
        ('Porto Espacial Central', 'Coruscant', 'Principal hub de transporte da galaxia')
        ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

        -- NABOO - Adicionar mais cidades
        INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
        ('Keren', 'Naboo', 'Cidade montanhosa de Naboo'),
        ('Moenia', 'Naboo', 'Cidade costeira de pescadores')
        ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

        -- KASHYYYK - Adicionar mais cidades
        INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
        ('Floresta Sombria', 'Kashyyyk', 'Regiao perigosa da floresta'),
        ('Vila das Pontes', 'Kashyyyk', 'Pequena comunidade conectada por pontes')
        ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

        -- HOTH - Adicionar mais cidades
        INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
        ('Planicie Gelada', 'Hoth', 'Vasta extensao de gelo e neve'),
        ('Cavernas de Gelo', 'Hoth', 'Sistema de cavernas congeladas')
        ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;
    """)
    
    # Adicionar setores básicos para as novas cidades
    op.execute("""
        -- Setores para Anchorhead
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Centro de Mineracao', id_cidade, 'industrial', 2, 'Operacoes de mineracao de umidade'
        FROM Cidade WHERE nome_cidade = 'Anchorhead' AND nome_planeta = 'Tatooine'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Mercado Local', id_cidade, 'comercial', 1, 'Pequeno mercado para suprimentos'
        FROM Cidade WHERE nome_cidade = 'Anchorhead' AND nome_planeta = 'Tatooine'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Bestine
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Palacio do Governador', id_cidade, 'administrativo', 1, 'Sede do governo planetario'
        FROM Cidade WHERE nome_cidade = 'Bestine' AND nome_planeta = 'Tatooine'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Quartel Imperial', id_cidade, 'militar', 3, 'Base das tropas imperiais'
        FROM Cidade WHERE nome_cidade = 'Bestine' AND nome_planeta = 'Tatooine'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Distrito Senatorial
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Residencias Senatoriais', id_cidade, 'residencial', 1, 'Casas dos senadores'
        FROM Cidade WHERE nome_cidade = 'Distrito Senatorial' AND nome_planeta = 'Coruscant'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Senado Galactico', id_cidade, 'administrativo', 1, 'Edificio do senado'
        FROM Cidade WHERE nome_cidade = 'Distrito Senatorial' AND nome_planeta = 'Coruscant'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Porto Espacial Central
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Terminal de Passageiros', id_cidade, 'comercial', 2, 'Area de embarque e desembarque'
        FROM Cidade WHERE nome_cidade = 'Porto Espacial Central' AND nome_planeta = 'Coruscant'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Hangares de Carga', id_cidade, 'industrial', 3, 'Depositos de mercadorias'
        FROM Cidade WHERE nome_cidade = 'Porto Espacial Central' AND nome_planeta = 'Coruscant'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Keren
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Observatorio', id_cidade, 'cientifico', 1, 'Centro de observacao astronomica'
        FROM Cidade WHERE nome_cidade = 'Keren' AND nome_planeta = 'Naboo'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Trilhas Montanhosas', id_cidade, 'natural', 2, 'Caminhos nas montanhas'
        FROM Cidade WHERE nome_cidade = 'Keren' AND nome_planeta = 'Naboo'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Moenia
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Porto de Pesca', id_cidade, 'comercial', 2, 'Mercado de peixes e frutos do mar'
        FROM Cidade WHERE nome_cidade = 'Moenia' AND nome_planeta = 'Naboo'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Praia Dourada', id_cidade, 'turistico', 1, 'Bela praia para relaxamento'
        FROM Cidade WHERE nome_cidade = 'Moenia' AND nome_planeta = 'Naboo'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Floresta Sombria
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Raizes Profundas', id_cidade, 'perigoso', 5, 'Nivel do solo da floresta'
        FROM Cidade WHERE nome_cidade = 'Floresta Sombria' AND nome_planeta = 'Kashyyyk'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Cavernas Ocultas', id_cidade, 'perigoso', 4, 'Cavernas com criaturas perigosas'
        FROM Cidade WHERE nome_cidade = 'Floresta Sombria' AND nome_planeta = 'Kashyyyk'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Vila das Pontes
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Ponte Principal', id_cidade, 'residencial', 2, 'Ponte central da comunidade'
        FROM Cidade WHERE nome_cidade = 'Vila das Pontes' AND nome_planeta = 'Kashyyyk'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Plataforma de Caca', id_cidade, 'comercial', 3, 'Area de preparacao para cacadas'
        FROM Cidade WHERE nome_cidade = 'Vila das Pontes' AND nome_planeta = 'Kashyyyk'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Planicie Gelada
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Campo de Gelo Norte', id_cidade, 'natural', 4, 'Planicie gelada com tempestades'
        FROM Cidade WHERE nome_cidade = 'Planicie Gelada' AND nome_planeta = 'Hoth'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Destrocos de Nave', id_cidade, 'perigoso', 3, 'Restos de naves acidentadas'
        FROM Cidade WHERE nome_cidade = 'Planicie Gelada' AND nome_planeta = 'Hoth'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

        -- Setores para Cavernas de Gelo
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Tunel Principal', id_cidade, 'natural', 3, 'Passagem principal das cavernas'
        FROM Cidade WHERE nome_cidade = 'Cavernas de Gelo' AND nome_planeta = 'Hoth'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
        
        INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) 
        SELECT 'Camara Profunda', id_cidade, 'perigoso', 4, 'Camara mais profunda com criaturas'
        FROM Cidade WHERE nome_cidade = 'Cavernas de Gelo' AND nome_planeta = 'Hoth'
        ON CONFLICT (nome_setor, id_cidade) DO NOTHING;
    """)

def downgrade():
    # Remover setores e cidades adicionados
    op.execute("""
        DELETE FROM Setor WHERE id_cidade IN (
            SELECT id_cidade FROM Cidade WHERE nome_cidade IN (
                'Anchorhead', 'Bestine',
                'Distrito Senatorial', 'Porto Espacial Central',
                'Keren', 'Moenia',
                'Floresta Sombria', 'Vila das Pontes',
                'Planicie Gelada', 'Cavernas de Gelo'
            )
        );
        
        DELETE FROM Cidade WHERE nome_cidade IN (
            'Anchorhead', 'Bestine',
            'Distrito Senatorial', 'Porto Espacial Central',
            'Keren', 'Moenia',
            'Floresta Sombria', 'Vila das Pontes',
            'Planicie Gelada', 'Cavernas de Gelo'
        );
    """)
