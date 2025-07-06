"""Implementar tipos de mob (Normal/Elite/Boss) na interface do jogo

Revision ID: 030
Revises: 029
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '030'
down_revision = '029'
branch_labels = None
depends_on = None

def upgrade():
    # Criar função para obter tipo do mob
    op.execute("""
        CREATE OR REPLACE FUNCTION obter_tipo_mob(tipo_mob_param VARCHAR(22))
        RETURNS VARCHAR(10) AS $$
        BEGIN
            -- Verificar se é Normal
            IF EXISTS (SELECT 1 FROM Normal WHERE tipo_mob = tipo_mob_param) THEN
                RETURN 'Normal';
            END IF;
            
            -- Verificar se é Elite
            IF EXISTS (SELECT 1 FROM Elite WHERE tipo_mob = tipo_mob_param) THEN
                RETURN 'Elite';
            END IF;
            
            -- Verificar se é Boss
            IF EXISTS (SELECT 1 FROM Boss WHERE tipo_mob = tipo_mob_param) THEN
                RETURN 'Boss';
            END IF;
            
            -- Se não encontrou em nenhuma, retornar Unknown
            RETURN 'Unknown';
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Atualizar função listar_inimigos_planeta para incluir tipo
    op.execute("""
        DROP FUNCTION IF EXISTS listar_inimigos_planeta(INT);
        CREATE OR REPLACE FUNCTION listar_inimigos_planeta(jogador_id INT)
        RETURNS TABLE (
            id_mob INT,
            tipo_mob VARCHAR(22),
            vida_base INT,
            nivel INT,
            dano_base INT,
            pontos_escudo INT,
            creditos INT,
            nivel_ameaca INT,
            categoria_mob VARCHAR(10)
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                i.id_mob,
                i.tipo_mob,
                i.vida_base,
                i.nivel,
                i.dano_base,
                i.pontos_escudo,
                i.creditos,
                m.nivel_ameaca,
                obter_tipo_mob(i.tipo_mob) AS categoria_mob
            FROM Inimigo i
            JOIN MOB m ON i.tipo_mob = m.tipo_mob
            JOIN Personagem p ON p.nome_planeta = i.planeta_origem
            WHERE p.id_player = jogador_id
            ORDER BY 
                CASE obter_tipo_mob(i.tipo_mob)
                    WHEN 'Normal' THEN 1
                    WHEN 'Elite' THEN 2
                    WHEN 'Boss' THEN 3
                    ELSE 4
                END,
                m.nivel_ameaca, 
                i.nivel;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Atualizar função listar_inimigos_setor_jogador para incluir tipo
    op.execute("""
        DROP FUNCTION IF EXISTS listar_inimigos_setor_jogador(INT);
        CREATE OR REPLACE FUNCTION listar_inimigos_setor_jogador(jogador_id INT)
        RETURNS TABLE (
            id_mob INT,
            tipo_mob VARCHAR(22),
            vida_base INT,
            nivel INT,
            dano_base INT,
            pontos_escudo INT,
            creditos INT,
            nivel_ameaca INT,
            categoria_mob VARCHAR(10)
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT
                i.id_mob,
                i.tipo_mob,
                i.vida_base,
                i.nivel,
                i.dano_base,
                i.pontos_escudo,
                i.creditos,
                m.nivel_ameaca,
                obter_tipo_mob(i.tipo_mob) AS categoria_mob
            FROM Inimigo i
            JOIN MOB m ON i.tipo_mob = m.tipo_mob
            JOIN Inimigo_Setor ins ON i.id_mob = ins.id_mob
            JOIN Personagem p ON p.id_setor = ins.id_setor
            WHERE p.id_player = jogador_id
            ORDER BY 
                CASE obter_tipo_mob(i.tipo_mob)
                    WHEN 'Normal' THEN 1
                    WHEN 'Elite' THEN 2
                    WHEN 'Boss' THEN 3
                    ELSE 4
                END,
                m.nivel_ameaca, 
                i.nivel;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Criar função para obter características especiais do mob
    op.execute("""
        CREATE OR REPLACE FUNCTION obter_caracteristicas_mob(tipo_mob_param VARCHAR(22))
        RETURNS TEXT AS $$
        DECLARE
            caracteristicas TEXT := '';
            tipo_categoria VARCHAR(10);
        BEGIN
            tipo_categoria := obter_tipo_mob(tipo_mob_param);
            
            CASE tipo_categoria
                WHEN 'Normal' THEN
                    SELECT 
                        CASE 
                            WHEN Formacao_Tatica THEN 'Formação Tática, ' ELSE '' 
                        END ||
                        CASE 
                            WHEN Patrulha THEN 'Patrulha, ' ELSE '' 
                        END ||
                        CASE 
                            WHEN Ataque_Coordenado THEN 'Ataque Coordenado' ELSE '' 
                        END
                    INTO caracteristicas
                    FROM Normal WHERE tipo_mob = tipo_mob_param;
                    
                WHEN 'Elite' THEN
                    SELECT 
                        CASE 
                            WHEN Armadura_Reforçada THEN 'Armadura Reforçada, ' ELSE '' 
                        END ||
                        CASE 
                            WHEN Ataque_Especial THEN 'Ataque Especial, ' ELSE '' 
                        END ||
                        CASE 
                            WHEN Regeneracao THEN 'Regeneração' ELSE '' 
                        END
                    INTO caracteristicas
                    FROM Elite WHERE tipo_mob = tipo_mob_param;
                    
                WHEN 'Boss' THEN
                    SELECT 
                        'Arsenal: ' || Arsenal ||
                        CASE 
                            WHEN Habilidade_Unica THEN ', Habilidade Única' ELSE '' 
                        END ||
                        CASE 
                            WHEN Invocacao_Aliados THEN ', Invoca Aliados' ELSE '' 
                        END
                    INTO caracteristicas
                    FROM Boss WHERE tipo_mob = tipo_mob_param;
                    
                ELSE
                    caracteristicas := 'Características desconhecidas';
            END CASE;
            
            -- Remover vírgulas extras no final
            caracteristicas := TRIM(TRAILING ', ' FROM caracteristicas);
            
            IF caracteristicas = '' THEN
                caracteristicas := 'Nenhuma característica especial';
            END IF;
            
            RETURN caracteristicas;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover funções criadas
    op.execute("""
        DROP FUNCTION IF EXISTS obter_caracteristicas_mob(VARCHAR(22));
        DROP FUNCTION IF EXISTS obter_tipo_mob(VARCHAR(22));
    """)
    
    # Reverter função listar_inimigos_planeta para versão anterior
    op.execute("""
        DROP FUNCTION IF EXISTS listar_inimigos_planeta(INT);
        CREATE OR REPLACE FUNCTION listar_inimigos_planeta(jogador_id INT)
        RETURNS TABLE (
            id_mob INT,
            tipo_mob VARCHAR(22),
            vida_base INT,
            nivel INT,
            dano_base INT,
            pontos_escudo INT,
            creditos INT,
            nivel_ameaca INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                i.id_mob,
                i.tipo_mob,
                i.vida_base,
                i.nivel,
                i.dano_base,
                i.pontos_escudo,
                i.creditos,
                m.nivel_ameaca
            FROM Inimigo i
            JOIN MOB m ON i.tipo_mob = m.tipo_mob
            JOIN Personagem p ON p.nome_planeta = i.planeta_origem
            WHERE p.id_player = jogador_id
            ORDER BY m.nivel_ameaca, i.nivel;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Reverter função listar_inimigos_setor_jogador para versão anterior
    op.execute("""
        DROP FUNCTION IF EXISTS listar_inimigos_setor_jogador(INT);
        CREATE OR REPLACE FUNCTION listar_inimigos_setor_jogador(jogador_id INT)
        RETURNS TABLE (
            id_mob INT,
            tipo_mob VARCHAR(22),
            vida_base INT,
            nivel INT,
            dano_base INT,
            pontos_escudo INT,
            creditos INT,
            nivel_ameaca INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT
                i.id_mob,
                i.tipo_mob,
                i.vida_base,
                i.nivel,
                i.dano_base,
                i.pontos_escudo,
                i.creditos,
                m.nivel_ameaca
            FROM Inimigo i
            JOIN MOB m ON i.tipo_mob = m.tipo_mob
            JOIN Inimigo_Setor ins ON i.id_mob = ins.id_mob
            JOIN Personagem p ON p.id_setor = ins.id_setor
            WHERE p.id_player = jogador_id
            ORDER BY m.nivel_ameaca, i.nivel;
        END;
        $$ LANGUAGE plpgsql;
    """)
