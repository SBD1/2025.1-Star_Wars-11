"""Sistema de ataques especiais por classe e expansão de cidades/setores

Revision ID: 020
Revises: 019
Create Date: 2025-07-06

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '020'
down_revision = '019'
branch_labels = None
depends_on = None

def upgrade():
    # Criar tabela de ataques especiais
    op.execute("""
        CREATE TABLE IF NOT EXISTS Ataque_Especial (
            id_ataque INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            nome_ataque VARCHAR(50) NOT NULL,
            descricao TEXT NOT NULL,
            dano_base INT NOT NULL,
            custo_mana INT DEFAULT 0,
            cooldown_turnos INT DEFAULT 0,
            nivel_requerido INT NOT NULL DEFAULT 1,
            nome_classe VARCHAR(22) NOT NULL,
            tipo_ataque VARCHAR(20) DEFAULT 'fisico', -- fisico, forca, tecnologico
            efeito_especial TEXT,
            FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe),
            UNIQUE(nome_ataque, nome_classe)
        );
    """)
    
    # Criar tabela de ataques conhecidos pelo jogador
    op.execute("""
        CREATE TABLE IF NOT EXISTS Personagem_Ataque (
            id_player INT NOT NULL,
            id_ataque INT NOT NULL,
            nivel_desbloqueio INT NOT NULL,
            data_desbloqueio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id_player, id_ataque),
            FOREIGN KEY (id_player) REFERENCES Personagem(id_player) ON DELETE CASCADE,
            FOREIGN KEY (id_ataque) REFERENCES Ataque_Especial(id_ataque) ON DELETE CASCADE
        );
    """)
    
    # Adicionar coluna mana_atual ao Personagem (para ataques especiais)
    op.add_column('personagem', sa.Column('mana_atual', sa.Integer(), nullable=False, server_default='50'))
    op.add_column('personagem', sa.Column('mana_base', sa.Integer(), nullable=False, server_default='50'))
    
    # Inserir ataques especiais para cada classe
    op.execute("""
        -- ATAQUES JEDI
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Golpe de Sabre', 'Ataque básico com sabre de luz', 25, 0, 1, 'Jedi', 'fisico', 'Sempre disponível'),
        ('Empurrão da Força', 'Empurra o inimigo causando dano', 20, 10, 3, 'Jedi', 'forca', 'Pode atordoar por 1 turno'),
        ('Cura da Força', 'Restaura vida usando a Força', 0, 15, 5, 'Jedi', 'forca', 'Cura 30 pontos de vida'),
        ('Reflexão de Blaster', 'Reflete ataques à distância', 15, 8, 7, 'Jedi', 'forca', 'Reflete 50% do dano recebido'),
        ('Golpe Devastador', 'Ataque poderoso com sabre duplo', 45, 20, 10, 'Jedi', 'fisico', 'Ignora 25% da defesa');
        
        -- ATAQUES SITH
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Golpe Sombrio', 'Ataque básico com sabre vermelho', 25, 0, 1, 'Sith', 'fisico', 'Sempre disponível'),
        ('Raio da Força', 'Dispara raios de energia sombria', 30, 12, 3, 'Sith', 'forca', 'Pode causar paralisia'),
        ('Drenar Vida', 'Absorve vida do inimigo', 20, 15, 5, 'Sith', 'forca', 'Cura 50% do dano causado'),
        ('Fúria Sith', 'Aumenta dano por 3 turnos', 0, 18, 7, 'Sith', 'forca', 'Dobra o dano dos próximos ataques'),
        ('Tempestade de Raios', 'Múltiplos raios devastadores', 50, 25, 10, 'Sith', 'forca', 'Ataque em área');
        
        -- ATAQUES CAÇADOR DE RECOMPENSAS
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Tiro Certeiro', 'Disparo básico com blaster', 22, 0, 1, 'Cacador_de_Recompensas', 'tecnologico', 'Sempre disponível'),
        ('Granada Atordoante', 'Granada que causa dano e atordoa', 25, 8, 3, 'Cacador_de_Recompensas', 'tecnologico', 'Atordoa por 2 turnos'),
        ('Tiro Duplo', 'Dois disparos rápidos', 35, 12, 5, 'Cacador_de_Recompensas', 'tecnologico', 'Dois ataques em sequência'),
        ('Míssil Teleguiado', 'Míssil que sempre acerta', 40, 15, 7, 'Cacador_de_Recompensas', 'tecnologico', 'Nunca erra o alvo'),
        ('Chuva de Blasters', 'Rajada devastadora', 55, 22, 10, 'Cacador_de_Recompensas', 'tecnologico', 'Múltiplos disparos');
    """)
    
    # Função para desbloquear ataques automaticamente ao subir de nível
    op.execute("""
        CREATE OR REPLACE FUNCTION desbloquear_ataques_nivel(jogador_id INT, novo_nivel INT)
        RETURNS TEXT AS $$
        DECLARE
            classe_jogador VARCHAR(22);
            ataques_desbloqueados INT := 0;
            ataque_record RECORD;
        BEGIN
            -- Obter classe do jogador
            SELECT nome_classe INTO classe_jogador
            FROM Personagem WHERE id_player = jogador_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Jogador não encontrado';
            END IF;
            
            -- Desbloquear ataques disponíveis para o nível
            FOR ataque_record IN 
                SELECT ae.id_ataque, ae.nome_ataque, ae.nivel_requerido
                FROM Ataque_Especial ae
                WHERE ae.nome_classe = classe_jogador 
                AND ae.nivel_requerido <= novo_nivel
                AND NOT EXISTS (
                    SELECT 1 FROM Personagem_Ataque pa 
                    WHERE pa.id_player = jogador_id AND pa.id_ataque = ae.id_ataque
                )
            LOOP
                INSERT INTO Personagem_Ataque (id_player, id_ataque, nivel_desbloqueio)
                VALUES (jogador_id, ataque_record.id_ataque, ataque_record.nivel_requerido);
                
                ataques_desbloqueados := ataques_desbloqueados + 1;
            END LOOP;
            
            IF ataques_desbloqueados > 0 THEN
                RETURN 'Desbloqueados ' || ataques_desbloqueados || ' novos ataques especiais!';
            ELSE
                RETURN 'Nenhum novo ataque desbloqueado neste nível.';
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Função para listar ataques disponíveis do jogador
    op.execute("""
        CREATE OR REPLACE FUNCTION listar_ataques_jogador(jogador_id INT)
        RETURNS TABLE(
            id_ataque INT,
            nome_ataque VARCHAR(50),
            descricao TEXT,
            dano_base INT,
            custo_mana INT,
            tipo_ataque VARCHAR(20),
            efeito_especial TEXT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                ae.id_ataque,
                ae.nome_ataque,
                ae.descricao,
                ae.dano_base,
                ae.custo_mana,
                ae.tipo_ataque,
                ae.efeito_especial
            FROM Ataque_Especial ae
            INNER JOIN Personagem_Ataque pa ON ae.id_ataque = pa.id_ataque
            WHERE pa.id_player = jogador_id
            ORDER BY ae.nivel_requerido, ae.nome_ataque;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover funções
    op.execute("DROP FUNCTION IF EXISTS listar_ataques_jogador(INT);")
    op.execute("DROP FUNCTION IF EXISTS desbloquear_ataques_nivel(INT, INT);")
    
    # Remover colunas
    op.drop_column('personagem', 'mana_atual')
    op.drop_column('personagem', 'mana_base')
    
    # Remover tabelas
    op.execute("DROP TABLE IF EXISTS Personagem_Ataque CASCADE;")
    op.execute("DROP TABLE IF EXISTS Ataque_Especial CASCADE;")
