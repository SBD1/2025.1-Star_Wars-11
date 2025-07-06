"""Corrigir tamanho VARCHAR para classe_atacante na função calcular_dano

Revision ID: 026
Revises: 025
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '026'
down_revision = '025'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir função calcular_dano para suportar nomes de classe maiores
    op.execute("""
        -- Recriar função calcular_dano com VARCHAR(50) para classe
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        CREATE OR REPLACE FUNCTION calcular_dano(atacante_id INT, eh_jogador BOOLEAN)
        RETURNS INT AS $$
        DECLARE
            dano_base_jogador INT := 10;
            dano_base_inimigo INT;
            level_atacante INT;
            classe_atacante VARCHAR(50);  -- Aumentado de 20 para 50
            modificador_classe INT := 0;
            dano_final INT;
            chance_critico INT;
        BEGIN
            IF eh_jogador THEN
                -- Obter dados do jogador
                SELECT level, nome_classe INTO level_atacante, classe_atacante
                FROM Personagem WHERE id_player = atacante_id;
                
                -- Modificadores por classe
                CASE classe_atacante
                    WHEN 'Jedi' THEN modificador_classe := 5;
                    WHEN 'Sith' THEN modificador_classe := 7;
                    WHEN 'Cacador_de_Recompensas' THEN modificador_classe := 3;
                    ELSE modificador_classe := 0;
                END CASE;
                
                -- Calcular dano base + level + modificador de classe
                dano_final := dano_base_jogador + (level_atacante * 2) + modificador_classe;
                
                -- Chance de crítico (10% base + 2% por level)
                chance_critico := 10 + (level_atacante * 2);
                IF random() * 100 < chance_critico THEN
                    dano_final := dano_final * 2;
                END IF;
                
            ELSE
                -- Para inimigos, usar dano base do inimigo
                SELECT dano_base INTO dano_base_inimigo
                FROM Inimigo WHERE id_mob = atacante_id;
                
                -- Variação de ±20% no dano
                dano_final := dano_base_inimigo + (random() * 0.4 - 0.2) * dano_base_inimigo;
                dano_final := GREATEST(dano_final, 1); -- Mínimo 1 de dano
            END IF;
            
            RETURN dano_final;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para VARCHAR(20)
    op.execute("""
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        CREATE OR REPLACE FUNCTION calcular_dano(atacante_id INT, eh_jogador BOOLEAN)
        RETURNS INT AS $$
        DECLARE
            dano_base_jogador INT := 10;
            dano_base_inimigo INT;
            level_atacante INT;
            classe_atacante VARCHAR(20);
            modificador_classe INT := 0;
            dano_final INT;
            chance_critico INT;
        BEGIN
            IF eh_jogador THEN
                -- Obter dados do jogador
                SELECT level, nome_classe INTO level_atacante, classe_atacante
                FROM Personagem WHERE id_player = atacante_id;
                
                -- Modificadores por classe
                CASE classe_atacante
                    WHEN 'Jedi' THEN modificador_classe := 5;
                    WHEN 'Sith' THEN modificador_classe := 7;
                    WHEN 'Cacador_de_Recompensas' THEN modificador_classe := 3;
                    ELSE modificador_classe := 0;
                END CASE;
                
                -- Calcular dano base + level + modificador de classe
                dano_final := dano_base_jogador + (level_atacante * 2) + modificador_classe;
                
                -- Chance de crítico (10% base + 2% por level)
                chance_critico := 10 + (level_atacante * 2);
                IF random() * 100 < chance_critico THEN
                    dano_final := dano_final * 2;
                END IF;
                
            ELSE
                -- Para inimigos, usar dano base do inimigo
                SELECT dano_base INTO dano_base_inimigo
                FROM Inimigo WHERE id_mob = atacante_id;
                
                -- Variação de ±20% no dano
                dano_final := dano_base_inimigo + (random() * 0.4 - 0.2) * dano_base_inimigo;
                dano_final := GREATEST(dano_final, 1); -- Mínimo 1 de dano
            END IF;
            
            RETURN dano_final;
        END;
        $$ LANGUAGE plpgsql;
    """)
