"""Sistema de cron job para respawn automático via triggers

Revision ID: 040
Revises: 039
Create Date: 2025-07-08

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '040'
down_revision = '039'
branch_labels = None
depends_on = None

def upgrade():
    # =====================================================
    # SISTEMA DE CRON JOB VIA TRIGGERS TEMPORAIS
    # =====================================================
    
    # Criar tabela de controle de jobs automáticos
    op.execute("""
        CREATE TABLE IF NOT EXISTS Sistema_Cron_Jobs (
            id_job INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
            nome_job VARCHAR(50) NOT NULL UNIQUE,
            descricao TEXT,
            intervalo_segundos INT NOT NULL,
            ultima_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            proxima_execucao TIMESTAMP,
            ativo BOOLEAN DEFAULT true,
            contador_execucoes INT DEFAULT 0,
            contador_erros INT DEFAULT 0
        );
    """)
    
    # Inserir job de respawn de mobs
    op.execute("""
        INSERT INTO Sistema_Cron_Jobs (nome_job, descricao, intervalo_segundos, proxima_execucao) VALUES
        ('respawn_mobs', 'Processamento automático de respawn de mobs', 30, CURRENT_TIMESTAMP + INTERVAL '30 seconds'),
        ('limpeza_logs', 'Limpeza de logs antigos do sistema', 3600, CURRENT_TIMESTAMP + INTERVAL '1 hour'),
        ('backup_economia', 'Backup dos dados econômicos', 1800, CURRENT_TIMESTAMP + INTERVAL '30 minutes');
    """)
    
    # Função principal do sistema de cron
    op.execute("""
        CREATE OR REPLACE FUNCTION executar_sistema_cron()
        RETURNS VOID AS $$
        DECLARE
            job_record RECORD;
            resultado TEXT;
            erro_msg TEXT;
        BEGIN
            -- Processar todos os jobs que precisam ser executados
            FOR job_record IN 
                SELECT * FROM Sistema_Cron_Jobs 
                WHERE ativo = true 
                AND proxima_execucao <= CURRENT_TIMESTAMP
            LOOP
                BEGIN
                    -- Executar job específico baseado no nome
                    CASE job_record.nome_job
                        WHEN 'respawn_mobs' THEN
                            PERFORM processar_respawn_mobs();
                            resultado := 'Respawn de mobs processado com sucesso';
                            
                        WHEN 'limpeza_logs' THEN
                            PERFORM limpar_logs_antigos();
                            resultado := 'Limpeza de logs executada';
                            
                        WHEN 'backup_economia' THEN
                            PERFORM backup_dados_economia();
                            resultado := 'Backup econômico realizado';
                            
                        ELSE
                            resultado := 'Job não reconhecido: ' || job_record.nome_job;
                    END CASE;
                    
                    -- Atualizar controle do job (sucesso)
                    UPDATE Sistema_Cron_Jobs 
                    SET ultima_execucao = CURRENT_TIMESTAMP,
                        proxima_execucao = CURRENT_TIMESTAMP + INTERVAL '1 second' * intervalo_segundos,
                        contador_execucoes = contador_execucoes + 1
                    WHERE id_job = job_record.id_job;
                    
                    -- Log de sucesso
                    INSERT INTO Sistema_Log (evento, descricao) VALUES
                    ('cron_job_sucesso', 'Job ' || job_record.nome_job || ': ' || resultado);
                    
                EXCEPTION
                    WHEN OTHERS THEN
                        erro_msg := SQLERRM;
                        
                        -- Atualizar controle do job (erro)
                        UPDATE Sistema_Cron_Jobs 
                        SET ultima_execucao = CURRENT_TIMESTAMP,
                            proxima_execucao = CURRENT_TIMESTAMP + INTERVAL '1 second' * (intervalo_segundos * 2), -- Dobrar intervalo em caso de erro
                            contador_erros = contador_erros + 1
                        WHERE id_job = job_record.id_job;
                        
                        -- Log de erro
                        INSERT INTO Sistema_Log (evento, descricao) VALUES
                        ('cron_job_erro', 'Job ' || job_record.nome_job || ' falhou: ' || erro_msg);
                END;
            END LOOP;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Função para limpeza de logs antigos
    op.execute("""
        CREATE OR REPLACE FUNCTION limpar_logs_antigos()
        RETURNS VOID AS $$
        DECLARE
            logs_removidos INT;
        BEGIN
            -- Remover logs mais antigos que 7 dias
            DELETE FROM Sistema_Log 
            WHERE timestamp_evento < CURRENT_TIMESTAMP - INTERVAL '7 days';
            
            GET DIAGNOSTICS logs_removidos = ROW_COUNT;
            
            -- Log da limpeza
            INSERT INTO Sistema_Log (evento, descricao) VALUES
            ('limpeza_logs', 'Removidos ' || logs_removidos || ' logs antigos');
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Função para backup de dados econômicos
    op.execute("""
        CREATE OR REPLACE FUNCTION backup_dados_economia()
        RETURNS VOID AS $$
        DECLARE
            total_gcs BIGINT;
            total_jogadores INT;
            total_naves INT;
        BEGIN
            -- Calcular estatísticas econômicas
            SELECT SUM(gcs), COUNT(*) INTO total_gcs, total_jogadores FROM Personagem;
            SELECT COUNT(*) INTO total_naves FROM Nave WHERE Id_Player IS NOT NULL;
            
            -- Inserir snapshot econômico
            INSERT INTO Sistema_Log (evento, descricao) VALUES
            ('backup_economia', 
             'Snapshot econômico - Total GCS: ' || COALESCE(total_gcs, 0) || 
             ', Jogadores: ' || total_jogadores || 
             ', Naves: ' || total_naves);
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # =====================================================
    # TRIGGERS PARA EXECUÇÃO AUTOMÁTICA
    # =====================================================
    
    # Trigger que executa o cron a cada inserção/atualização em tabelas específicas
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_executar_cron()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Executar cron apenas se passou tempo suficiente desde a última execução
            IF NOT EXISTS (
                SELECT 1 FROM Sistema_Cron_Jobs 
                WHERE nome_job = 'respawn_mobs' 
                AND ultima_execucao > CURRENT_TIMESTAMP - INTERVAL '25 seconds'
            ) THEN
                PERFORM executar_sistema_cron();
            END IF;
            
            RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Aplicar trigger em tabelas relevantes
    op.execute("""
        -- Trigger em combates finalizados (para processar respawn)
        DROP TRIGGER IF EXISTS trigger_cron_combate ON Combate_Resultado;
        CREATE TRIGGER trigger_cron_combate
            AFTER INSERT ON Combate_Resultado
            FOR EACH ROW
            EXECUTE FUNCTION trigger_executar_cron();
    """)
    
    # =====================================================
    # FUNÇÃO MANUAL PARA FORÇAR EXECUÇÃO DO CRON
    # =====================================================
    
    op.execute("""
        CREATE OR REPLACE FUNCTION executar_cron_manual()
        RETURNS TEXT AS $$
        DECLARE
            jobs_executados INT := 0;
        BEGIN
            -- Forçar execução de todos os jobs ativos
            UPDATE Sistema_Cron_Jobs 
            SET proxima_execucao = CURRENT_TIMESTAMP 
            WHERE ativo = true;
            
            GET DIAGNOSTICS jobs_executados = ROW_COUNT;
            
            -- Executar o cron
            PERFORM executar_sistema_cron();
            
            RETURN 'Cron executado manualmente. ' || jobs_executados || ' jobs processados.';
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # =====================================================
    # FUNÇÃO PARA MONITORAR STATUS DO SISTEMA
    # =====================================================
    
    op.execute("""
        CREATE OR REPLACE FUNCTION status_sistema_cron()
        RETURNS TABLE (
            nome_job VARCHAR(50),
            ativo BOOLEAN,
            ultima_execucao TIMESTAMP,
            proxima_execucao TIMESTAMP,
            execucoes INT,
            erros INT,
            status_saude TEXT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                scj.nome_job,
                scj.ativo,
                scj.ultima_execucao,
                scj.proxima_execucao,
                scj.contador_execucoes,
                scj.contador_erros,
                CASE 
                    WHEN NOT scj.ativo THEN 'INATIVO'
                    WHEN scj.contador_erros > scj.contador_execucoes * 0.1 THEN 'PROBLEMAS'
                    WHEN scj.proxima_execucao < CURRENT_TIMESTAMP - INTERVAL '5 minutes' THEN 'ATRASADO'
                    ELSE 'SAUDÁVEL'
                END as status_saude
            FROM Sistema_Cron_Jobs scj
            ORDER BY scj.nome_job;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover triggers
    op.execute("DROP TRIGGER IF EXISTS trigger_cron_combate ON Combate_Resultado;")
    
    # Remover funções
    op.execute("DROP FUNCTION IF EXISTS status_sistema_cron();")
    op.execute("DROP FUNCTION IF EXISTS executar_cron_manual();")
    op.execute("DROP FUNCTION IF EXISTS trigger_executar_cron();")
    op.execute("DROP FUNCTION IF EXISTS backup_dados_economia();")
    op.execute("DROP FUNCTION IF EXISTS limpar_logs_antigos();")
    op.execute("DROP FUNCTION IF EXISTS executar_sistema_cron();")
    
    # Remover tabela
    op.execute("DROP TABLE IF EXISTS Sistema_Cron_Jobs CASCADE;")
