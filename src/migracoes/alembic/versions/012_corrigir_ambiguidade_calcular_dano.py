"""Corrigir ambiguidade na função calcular_dano

Revision ID: 012
Revises: 1e65d57ce3df
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '012'
down_revision = '1e65d57ce3df'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir a função calcular_dano para resolver ambiguidade de variáveis
    op.execute("""
        -- Remover função existente
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        
        -- Recriar função com variáveis não ambíguas
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
                    WHEN 'Jedi' THEN modificador_classe := 8;
                    WHEN 'Sith' THEN modificador_classe := 10;
                    WHEN 'Soldado' THEN modificador_classe := 6;
                    WHEN 'Piloto' THEN modificador_classe := 4;
                    WHEN 'Contrabandista' THEN modificador_classe := 5;
                    ELSE modificador_classe := 3;
                END CASE;
            ELSE
                -- Obter dados do inimigo
                SELECT nivel, dano_base INTO level_atacante, dano_base_inimigo
                FROM Inimigo WHERE id_mob = atacante_id;
                modificador_classe := 0;
            END IF;
            
            -- Calculo base do dano (balanceado)
            IF eh_jogador THEN
                -- Jogador: dano base + level*3 + modificador classe
                dano_final := dano_base_jogador + (level_atacante * 3) + modificador_classe;
            ELSE
                -- Inimigo: dano base do inimigo + level*2
                dano_final := dano_base_inimigo + (level_atacante * 2);
            END IF;
            
            -- Chance de critico (5%)
            chance_critico := floor(random() * 100) + 1;
            IF chance_critico <= 5 THEN
                dano_final := dano_final * 2;
            END IF;
            
            -- Variacao aleatoria (±20%)
            dano_final := dano_final + floor(random() * (dano_final * 0.4)) - floor(dano_final * 0.2);
            
            -- Garantir dano minimo
            IF dano_final < 1 THEN
                dano_final := 1;
            END IF;
            
            RETURN dano_final;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para a versão anterior (com problema de ambiguidade)
    op.execute("""
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        
        CREATE OR REPLACE FUNCTION calcular_dano(atacante_id INT, eh_jogador BOOLEAN)
        RETURNS INT AS $$
        DECLARE
            dano_base INT := 10;
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
                    WHEN 'Jedi' THEN modificador_classe := 8;
                    WHEN 'Sith' THEN modificador_classe := 10;
                    WHEN 'Soldado' THEN modificador_classe := 6;
                    WHEN 'Piloto' THEN modificador_classe := 4;
                    WHEN 'Contrabandista' THEN modificador_classe := 5;
                    ELSE modificador_classe := 3;
                END CASE;
            ELSE
                -- Obter dados do inimigo (problema de ambiguidade aqui)
                SELECT nivel, dano_base INTO level_atacante, dano_base
                FROM Inimigo WHERE id_mob = atacante_id;
                modificador_classe := 0;
            END IF;
            
            -- Calculo base do dano (balanceado)
            IF eh_jogador THEN
                -- Jogador: dano base + level*3 + modificador classe
                dano_final := dano_base + (level_atacante * 3) + modificador_classe;
            ELSE
                -- Inimigo: dano base do inimigo + level*2
                dano_final := dano_base + (level_atacante * 2);
            END IF;
            
            -- Chance de critico (5%)
            chance_critico := floor(random() * 100) + 1;
            IF chance_critico <= 5 THEN
                dano_final := dano_final * 2;
            END IF;
            
            -- Variacao aleatoria (±20%)
            dano_final := dano_final + floor(random() * (dano_final * 0.4)) - floor(dano_final * 0.2);
            
            -- Garantir dano minimo
            IF dano_final < 1 THEN
                dano_final := 1;
            END IF;
            
            RETURN dano_final;
        END;
        $$ LANGUAGE plpgsql;
    """)
