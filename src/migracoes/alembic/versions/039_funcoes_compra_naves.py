"""Funções de compra e validação de naves

Revision ID: 039
Revises: 038
Create Date: 2025-07-08

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '039'
down_revision = '038'
branch_labels = None
depends_on = None

def upgrade():
    # =====================================================
    # TABELA DE LOG DO SISTEMA (se não existir)
    # =====================================================
    
    op.execute("""
        CREATE TABLE IF NOT EXISTS Sistema_Log (
            id_log INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            evento VARCHAR(50) NOT NULL,
            descricao TEXT,
            timestamp_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_player INT NULL,
            FOREIGN KEY (id_player) REFERENCES Personagem(id_player)
        );
    """)
    
    # =====================================================
    # FUNÇÕES DE VALIDAÇÃO E COMPRA DE NAVES
    # =====================================================
    
    # Função para listar naves disponíveis para compra
    op.execute("""
        CREATE OR REPLACE FUNCTION listar_naves_disponiveis(jogador_id INT)
        RETURNS TABLE (
            id_loja INT,
            nome_nave VARCHAR(50),
            preco INT,
            velocidade INT,
            capacidade INT,
            nivel_minimo INT,
            descricao TEXT,
            pode_comprar BOOLEAN,
            motivo_bloqueio TEXT
        ) AS $$
        DECLARE
            jogador_nivel INT;
            jogador_planeta VARCHAR(20);
            jogador_setor VARCHAR(50);
            jogador_gcs INT;
        BEGIN
            -- Obter dados do jogador
            SELECT p.level, p.nome_planeta, p.gcs INTO jogador_nivel, jogador_planeta, jogador_gcs
            FROM Personagem p WHERE p.id_player = jogador_id;
            
            -- Obter setor atual do jogador (assumindo que existe uma forma de obter)
            -- Por simplicidade, vamos assumir que o jogador está no setor principal
            
            RETURN QUERY
            SELECT 
                ln.id_loja_nave,
                ln.nome_comercial,
                ln.preco_gcs,
                ln.velocidade,
                ln.capacidade,
                ln.nivel_minimo,
                ln.descricao,
                CASE 
                    WHEN NOT ln.ativa THEN false
                    WHEN ln.nivel_minimo > jogador_nivel THEN false
                    WHEN ln.preco_gcs > jogador_gcs THEN false
                    WHEN ln.planeta_disponivel IS NOT NULL AND ln.planeta_disponivel != jogador_planeta THEN false
                    ELSE true
                END as pode_comprar,
                CASE 
                    WHEN NOT ln.ativa THEN 'Nave não disponível'
                    WHEN ln.nivel_minimo > jogador_nivel THEN 'Nível insuficiente (req: ' || ln.nivel_minimo || ')'
                    WHEN ln.preco_gcs > jogador_gcs THEN 'Créditos insuficientes'
                    WHEN ln.planeta_disponivel IS NOT NULL AND ln.planeta_disponivel != jogador_planeta THEN 'Disponível apenas em ' || ln.planeta_disponivel
                    ELSE 'Disponível para compra'
                END as motivo_bloqueio
            FROM Loja_Nave ln
            WHERE ln.ativa = true
            ORDER BY ln.preco_gcs ASC;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Função para comprar nave
    op.execute("""
        CREATE OR REPLACE FUNCTION comprar_nave(jogador_id INT, id_loja_nave INT)
        RETURNS TEXT AS $$
        DECLARE
            nave_info RECORD;
            jogador_info RECORD;
            novo_modelo VARCHAR(30);
            contador_modelo INT;
            resultado TEXT;
        BEGIN
            -- Obter informações da nave na loja
            SELECT * INTO nave_info FROM Loja_Nave WHERE id_loja_nave = id_loja_nave AND ativa = true;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Nave não encontrada ou não disponível';
            END IF;
            
            -- Obter informações do jogador
            SELECT * INTO jogador_info FROM Personagem WHERE id_player = jogador_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Jogador não encontrado';
            END IF;
            
            -- Validações
            IF jogador_info.level < nave_info.nivel_minimo THEN
                RETURN 'Erro: Nível insuficiente. Necessário nível ' || nave_info.nivel_minimo;
            END IF;
            
            IF jogador_info.gcs < nave_info.preco_gcs THEN
                RETURN 'Erro: Créditos insuficientes. Necessário ' || nave_info.preco_gcs || ' GCS';
            END IF;
            
            IF nave_info.planeta_disponivel IS NOT NULL AND nave_info.planeta_disponivel != jogador_info.nome_planeta THEN
                RETURN 'Erro: Esta nave só está disponível em ' || nave_info.planeta_disponivel;
            END IF;
            
            -- Gerar modelo único para a nova nave
            contador_modelo := 1;
            LOOP
                novo_modelo := nave_info.tipo_nave || '-' || LPAD(jogador_id::TEXT, 3, '0') || '-' || LPAD(contador_modelo::TEXT, 3, '0');
                
                -- Verificar se modelo já existe
                IF NOT EXISTS (SELECT 1 FROM Nave WHERE modelo = novo_modelo) THEN
                    EXIT;
                END IF;
                
                contador_modelo := contador_modelo + 1;
                
                -- Evitar loop infinito
                IF contador_modelo > 999 THEN
                    RETURN 'Erro: Não foi possível gerar modelo único para a nave';
                END IF;
            END LOOP;
            
            -- Iniciar transação
            BEGIN
                -- Debitar créditos do jogador
                UPDATE Personagem 
                SET gcs = gcs - nave_info.preco_gcs 
                WHERE id_player = jogador_id;
                
                -- Criar nova nave
                INSERT INTO Nave (modelo, Id_Player, velocidade, capacidade)
                VALUES (novo_modelo, jogador_id, nave_info.velocidade, nave_info.capacidade);
                
                -- Inserir na tabela específica do tipo de nave
                CASE nave_info.tipo_nave
                    WHEN 'X_WING_T65' THEN
                        INSERT INTO X_WING_T65 (modelo) VALUES (novo_modelo);
                    WHEN 'YT_1300' THEN
                        INSERT INTO YT_1300 (modelo) VALUES (novo_modelo);
                    WHEN 'Lambda_Class_Shuttle' THEN
                        INSERT INTO Lambda_Class_Shuttle (modelo) VALUES (novo_modelo);
                    WHEN 'Fregata_Corelliana_CR90' THEN
                        INSERT INTO Fregata_Corelliana_CR90 (modelo) VALUES (novo_modelo);
                    ELSE
                        RAISE EXCEPTION 'Tipo de nave não reconhecido: %', nave_info.tipo_nave;
                END CASE;
                
                -- Log da compra
                INSERT INTO Sistema_Log (evento, descricao, id_player) VALUES
                ('compra_nave', 
                 'Jogador comprou ' || nave_info.nome_comercial || ' por ' || nave_info.preco_gcs || ' GCS. Modelo: ' || novo_modelo,
                 jogador_id);
                
                resultado := 'Sucesso! Você comprou ' || nave_info.nome_comercial || ' por ' || nave_info.preco_gcs || ' GCS. Modelo: ' || novo_modelo;
                
            EXCEPTION
                WHEN OTHERS THEN
                    RETURN 'Erro na transação: ' || SQLERRM;
            END;
            
            RETURN resultado;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Função para vender nave (opcional)
    op.execute("""
        CREATE OR REPLACE FUNCTION vender_nave(jogador_id INT, modelo_nave VARCHAR(30))
        RETURNS TEXT AS $$
        DECLARE
            nave_info RECORD;
            valor_venda INT;
            tipo_nave_str VARCHAR(30);
        BEGIN
            -- Verificar se a nave pertence ao jogador
            SELECT * INTO nave_info FROM Nave WHERE modelo = modelo_nave AND Id_Player = jogador_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Nave não encontrada ou não pertence a você';
            END IF;
            
            -- Não permitir vender a última nave
            IF (SELECT COUNT(*) FROM Nave WHERE Id_Player = jogador_id) <= 1 THEN
                RETURN 'Erro: Você não pode vender sua única nave';
            END IF;
            
            -- Determinar tipo da nave e calcular valor de venda (50% do preço original)
            IF EXISTS (SELECT 1 FROM X_WING_T65 WHERE modelo = modelo_nave) THEN
                tipo_nave_str := 'X_WING_T65';
            ELSIF EXISTS (SELECT 1 FROM YT_1300 WHERE modelo = modelo_nave) THEN
                tipo_nave_str := 'YT_1300';
            ELSIF EXISTS (SELECT 1 FROM Lambda_Class_Shuttle WHERE modelo = modelo_nave) THEN
                tipo_nave_str := 'Lambda_Class_Shuttle';
            ELSIF EXISTS (SELECT 1 FROM Fregata_Corelliana_CR90 WHERE modelo = modelo_nave) THEN
                tipo_nave_str := 'Fregata_Corelliana_CR90';
            ELSE
                RETURN 'Erro: Tipo de nave não reconhecido';
            END IF;
            
            -- Obter preço médio da loja para este tipo (50% do valor)
            SELECT ROUND(AVG(preco_gcs) * 0.5) INTO valor_venda
            FROM Loja_Nave WHERE tipo_nave = tipo_nave_str;
            
            IF valor_venda IS NULL THEN
                valor_venda := 5000; -- Valor padrão
            END IF;
            
            -- Iniciar transação
            BEGIN
                -- Remover da tabela específica
                CASE tipo_nave_str
                    WHEN 'X_WING_T65' THEN
                        DELETE FROM X_WING_T65 WHERE modelo = modelo_nave;
                    WHEN 'YT_1300' THEN
                        DELETE FROM YT_1300 WHERE modelo = modelo_nave;
                    WHEN 'Lambda_Class_Shuttle' THEN
                        DELETE FROM Lambda_Class_Shuttle WHERE modelo = modelo_nave;
                    WHEN 'Fregata_Corelliana_CR90' THEN
                        DELETE FROM Fregata_Corelliana_CR90 WHERE modelo = modelo_nave;
                END CASE;
                
                -- Remover da tabela principal (CASCADE deve cuidar das referências)
                DELETE FROM Nave WHERE modelo = modelo_nave;
                
                -- Creditar valor da venda
                UPDATE Personagem 
                SET gcs = gcs + valor_venda 
                WHERE id_player = jogador_id;
                
                -- Log da venda
                INSERT INTO Sistema_Log (evento, descricao, id_player) VALUES
                ('venda_nave', 
                 'Jogador vendeu nave ' || modelo_nave || ' por ' || valor_venda || ' GCS',
                 jogador_id);
                
            EXCEPTION
                WHEN OTHERS THEN
                    RETURN 'Erro na transação: ' || SQLERRM;
            END;
            
            RETURN 'Sucesso! Você vendeu a nave ' || modelo_nave || ' por ' || valor_venda || ' GCS';
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover funções
    op.execute("DROP FUNCTION IF EXISTS vender_nave(INT, VARCHAR(30));")
    op.execute("DROP FUNCTION IF EXISTS comprar_nave(INT, INT);")
    op.execute("DROP FUNCTION IF EXISTS listar_naves_disponiveis(INT);")
    
    # Remover tabela de log (opcional, pode querer manter)
    # op.execute("DROP TABLE IF EXISTS Sistema_Log CASCADE;")
