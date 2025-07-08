"""Sistema de compra de naves e economia melhorada

Revision ID: 038
Revises: 037
Create Date: 2025-07-08

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '038'
down_revision = '037'
branch_labels = None
depends_on = None

def upgrade():
    # =====================================================
    # SISTEMA DE LOJA DE NAVES
    # =====================================================
    
    # Criar tabela de modelos de naves disponíveis para compra
    op.execute("""
        CREATE TABLE IF NOT EXISTS Loja_Nave (
            id_loja_nave INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            tipo_nave VARCHAR(30) NOT NULL, -- 'X_WING_T65', 'YT_1300', 'Lambda_Class_Shuttle', 'Fregata_Corelliana_CR90'
            nome_comercial VARCHAR(50) NOT NULL, -- Nome para exibição
            preco_gcs INT NOT NULL,
            velocidade INT NOT NULL,
            capacidade INT NOT NULL,
            nivel_minimo INT DEFAULT 1,
            planeta_disponivel VARCHAR(20), -- NULL = disponível em todos os planetas
            setor_disponivel VARCHAR(50), -- NULL = disponível em todos os setores do planeta
            descricao TEXT,
            ativa BOOLEAN DEFAULT true,
            FOREIGN KEY (planeta_disponivel) REFERENCES Planeta(nome_planeta)
        );
    """)
    
    # Popular loja com naves disponíveis
    op.execute("""
        INSERT INTO Loja_Nave (tipo_nave, nome_comercial, preco_gcs, velocidade, capacidade, nivel_minimo, planeta_disponivel, setor_disponivel, descricao) VALUES
        
        -- Naves básicas (disponíveis em Tatooine - planeta inicial)
        ('X_WING_T65', 'X-Wing T-65 Caça Estelar', 15000, 170, 1, 3, 'Tatooine', 'Hangar de Naves', 'Caça estelar rápido e ágil, ideal para combate espacial'),
        ('YT_1300', 'YT-1300 Cargueiro Modificado', 25000, 145, 5, 1, 'Tatooine', 'Hangar de Naves', 'Cargueiro versátil com boa capacidade de carga'),
        
        -- Naves intermediárias (Coruscant)
        ('Lambda_Class_Shuttle', 'Lambda Shuttle Imperial', 45000, 160, 20, 8, 'Coruscant', 'Estaleiro Imperial', 'Transporte militar com grande capacidade'),
        ('X_WING_T65', 'X-Wing T-65 Elite', 35000, 180, 1, 10, 'Coruscant', 'Base da Aliança', 'Versão melhorada do caça X-Wing'),
        
        -- Naves avançadas (Kashyyyk)
        ('Fregata_Corelliana_CR90', 'Fregata Corelliana CR90', 150000, 180, 100, 15, 'Kashyyyk', 'Estaleiro Wookiee', 'Nave capital com capacidade massiva'),
        ('YT_1300', 'Millennium Falcon Replica', 80000, 165, 8, 12, 'Kashyyyk', 'Estaleiro Wookiee', 'Réplica do famoso cargueiro com melhorias'),
        
        -- Naves especiais (Naboo)
        ('Lambda_Class_Shuttle', 'N-1 Starfighter Modificado', 60000, 200, 2, 12, 'Naboo', 'Hangar Real', 'Caça real de Naboo modificado para viagens'),
        
        -- Naves resistentes (Hoth)
        ('X_WING_T65', 'X-Wing Ártico', 40000, 160, 1, 8, 'Hoth', 'Base Echo', 'X-Wing adaptado para condições extremas');
    """)
    
    # =====================================================
    # AUMENTAR DROPS DE DINHEIRO DOS MOBS
    # =====================================================
    
    # Atualizar créditos dos mobs existentes (multiplicadores: Normal 2x, Elite 3x, Boss 5x)
    op.execute("""
        -- Mobs Normais (2x)
        UPDATE Inimigo SET creditos = creditos * 2 
        WHERE tipo_mob IN (
            SELECT tipo_mob FROM Normal
        );
        
        -- Mobs Elite (3x do valor original, então 1.5x do atual)
        UPDATE Inimigo SET creditos = ROUND(creditos * 1.5)
        WHERE tipo_mob IN (
            SELECT tipo_mob FROM Elite
        );
        
        -- Mobs Boss (5x do valor original, então 2.5x do atual)  
        UPDATE Inimigo SET creditos = ROUND(creditos * 2.5)
        WHERE tipo_mob IN (
            SELECT tipo_mob FROM Boss
        );
    """)
    
    # Adicionar sistema de drop variável (±25% do valor base)
    op.execute("""
        CREATE OR REPLACE FUNCTION calcular_drop_creditos(id_inimigo INT)
        RETURNS INT AS $$
        DECLARE
            creditos_base INT;
            variacao DECIMAL;
            creditos_final INT;
        BEGIN
            -- Obter créditos base do inimigo
            SELECT creditos INTO creditos_base
            FROM Inimigo WHERE id_mob = id_inimigo;
            
            IF creditos_base IS NULL THEN
                RETURN 0;
            END IF;
            
            -- Gerar variação aleatória entre 0.75 e 1.25 (±25%)
            variacao := 0.75 + (random() * 0.5);
            
            -- Calcular créditos finais
            creditos_final := ROUND(creditos_base * variacao);
            
            -- Garantir mínimo de 1 crédito
            IF creditos_final < 1 THEN
                creditos_final := 1;
            END IF;
            
            RETURN creditos_final;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # =====================================================
    # SISTEMA DE RESPAWN AUTOMÁTICO DE MOBS
    # =====================================================
    
    # Criar tabela para controlar respawn de mobs
    op.execute("""
        CREATE TABLE IF NOT EXISTS Mob_Respawn_Control (
            id_controle INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            id_inimigo_setor INT NOT NULL,
            quantidade_atual INT DEFAULT 0,
            ultimo_respawn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            proximo_respawn TIMESTAMP,
            ativo BOOLEAN DEFAULT true,
            FOREIGN KEY (id_inimigo_setor) REFERENCES Inimigo_Setor(id_inimigo_setor),
            UNIQUE(id_inimigo_setor)
        );
    """)
    
    # Popular controle de respawn para todos os inimigos em setores
    op.execute("""
        INSERT INTO Mob_Respawn_Control (id_inimigo_setor, quantidade_atual, proximo_respawn)
        SELECT
            ies.id_inimigo_setor,
            ies.quantidade_maxima, -- Começar com quantidade máxima
            CURRENT_TIMESTAMP + INTERVAL '1 second' * ies.taxa_respawn
        FROM Inimigo_Setor ies
        ON CONFLICT (id_inimigo_setor) DO NOTHING;
    """)

    # =====================================================
    # SISTEMA DE RESPAWN AUTOMÁTICO VIA TRIGGERS
    # =====================================================

    # Função para processar respawn de mobs
    op.execute("""
        CREATE OR REPLACE FUNCTION processar_respawn_mobs()
        RETURNS VOID AS $$
        DECLARE
            controle_record RECORD;
            novo_respawn TIMESTAMP;
        BEGIN
            -- Processar todos os controles que precisam de respawn
            FOR controle_record IN
                SELECT mrc.*, ies.quantidade_maxima, ies.taxa_respawn
                FROM Mob_Respawn_Control mrc
                JOIN Inimigo_Setor ies ON mrc.id_inimigo_setor = ies.id_inimigo_setor
                WHERE mrc.ativo = true
                AND mrc.proximo_respawn <= CURRENT_TIMESTAMP
                AND mrc.quantidade_atual < ies.quantidade_maxima
            LOOP
                -- Aumentar quantidade atual (respawn)
                UPDATE Mob_Respawn_Control
                SET quantidade_atual = LEAST(quantidade_atual + 1, controle_record.quantidade_maxima),
                    ultimo_respawn = CURRENT_TIMESTAMP,
                    proximo_respawn = CURRENT_TIMESTAMP + INTERVAL '1 second' * controle_record.taxa_respawn
                WHERE id_controle = controle_record.id_controle;

                -- Log do respawn (opcional)
                INSERT INTO Sistema_Log (evento, descricao, timestamp_evento) VALUES
                ('mob_respawn',
                 'Mob respawned - Controle ID: ' || controle_record.id_controle ||
                 ', Nova quantidade: ' || LEAST(controle_record.quantidade_atual + 1, controle_record.quantidade_maxima),
                 CURRENT_TIMESTAMP)
                ON CONFLICT DO NOTHING; -- Ignorar se tabela de log não existir
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Trigger para reduzir quantidade quando mob é morto
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_mob_morto()
        RETURNS TRIGGER AS $$
        DECLARE
            inimigo_setor_id INT;
        BEGIN
            -- Verificar se o combate foi vencido pelo jogador
            IF NEW.vencedor = 'jogador' THEN
                -- Encontrar o inimigo_setor correspondente
                SELECT ies.id_inimigo_setor INTO inimigo_setor_id
                FROM Inimigo_Setor ies
                WHERE ies.id_mob = NEW.id_mob
                LIMIT 1;

                -- Reduzir quantidade atual se encontrado
                IF inimigo_setor_id IS NOT NULL THEN
                    UPDATE Mob_Respawn_Control
                    SET quantidade_atual = GREATEST(quantidade_atual - 1, 0)
                    WHERE id_inimigo_setor = inimigo_setor_id;
                END IF;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    # Aplicar trigger na tabela de resultados de combate
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_mob_morto_respawn ON Combate_Resultado;
        CREATE TRIGGER trigger_mob_morto_respawn
            AFTER INSERT ON Combate_Resultado
            FOR EACH ROW
            EXECUTE FUNCTION trigger_mob_morto();
    """)

def downgrade():
    # Remover sistema de respawn
    op.execute("DROP TABLE IF EXISTS Mob_Respawn_Control CASCADE;")
    
    # Remover função de cálculo de drops
    op.execute("DROP FUNCTION IF EXISTS calcular_drop_creditos(INT);")
    
    # Reverter créditos dos mobs (dividir pelos multiplicadores)
    op.execute("""
        UPDATE Inimigo SET creditos = ROUND(creditos / 2.5)
        WHERE tipo_mob IN (SELECT tipo_mob FROM Boss);
        
        UPDATE Inimigo SET creditos = ROUND(creditos / 1.5)
        WHERE tipo_mob IN (SELECT tipo_mob FROM Elite);
        
        UPDATE Inimigo SET creditos = creditos / 2
        WHERE tipo_mob IN (SELECT tipo_mob FROM Normal);
    """)
    
    # Remover loja de naves
    op.execute("DROP TABLE IF EXISTS Loja_Nave CASCADE;")
