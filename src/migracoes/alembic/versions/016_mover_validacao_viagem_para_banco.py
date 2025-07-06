"""Mover validação de velocidade de viagem para o banco de dados

Revision ID: 016
Revises: 015
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '016'
down_revision = '015'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir a função viajar_para_planeta para incluir validação de velocidade
    op.execute("""
        -- Remover função existente
        DROP FUNCTION IF EXISTS viajar_para_planeta(INT, VARCHAR(20));
        
        -- Recriar função com validação de velocidade
        CREATE OR REPLACE FUNCTION viajar_para_planeta(jogador_id INT, planeta_destino VARCHAR(20))
        RETURNS TEXT AS $$
        DECLARE
            nave_jogador VARCHAR(20);
            velocidade_nave INT;
            velocidade_minima INT := 0;
            planeta_atual VARCHAR(20);
            primeira_cidade_id INT;
            nome_primeira_cidade VARCHAR(50);
            primeiro_setor_id INT;
            nome_primeiro_setor VARCHAR(50);
        BEGIN
            -- Verificar se o planeta existe
            IF NOT EXISTS (SELECT 1 FROM Planeta WHERE nome_planeta = planeta_destino) THEN
                RETURN 'Erro: Planeta nao encontrado';
            END IF;
            
            -- Obter dados do jogador
            SELECT nome_planeta, nome_nave INTO planeta_atual, nave_jogador
            FROM Personagem WHERE id_player = jogador_id;
            
            IF planeta_atual = planeta_destino THEN
                RETURN 'Erro: Voce ja esta neste planeta';
            END IF;
            
            -- Verificar se tem nave
            IF nave_jogador IS NULL THEN
                RETURN 'Erro: Voce precisa de uma nave para viajar entre planetas';
            END IF;
            
            -- Verificar velocidade da nave
            SELECT velocidade INTO velocidade_nave
            FROM Nave WHERE nome_nave = nave_jogador;
            
            -- Definir velocidade mínima necessária por planeta
            CASE planeta_destino
                WHEN 'Coruscant' THEN velocidade_minima := 150;
                WHEN 'Tatooine' THEN velocidade_minima := 100;
                ELSE velocidade_minima := 0;
            END CASE;
            
            -- Validar se a nave tem velocidade suficiente
            IF velocidade_nave < velocidade_minima THEN
                RETURN 'Erro: Sua nave e muito lenta para viajar para ' || planeta_destino || 
                       '. Velocidade necessaria: ' || velocidade_minima || 
                       ', sua nave tem: ' || velocidade_nave;
            END IF;
            
            -- Encontrar primeira cidade do planeta destino
            SELECT id_cidade, nome_cidade INTO primeira_cidade_id, nome_primeira_cidade
            FROM Cidade 
            WHERE nome_planeta = planeta_destino 
            ORDER BY id_cidade 
            LIMIT 1;
            
            IF primeira_cidade_id IS NULL THEN
                RETURN 'Erro: Este planeta nao possui cidades disponiveis';
            END IF;
            
            -- Encontrar primeiro setor da primeira cidade
            SELECT id_setor, nome_setor INTO primeiro_setor_id, nome_primeiro_setor
            FROM Setor 
            WHERE id_cidade = primeira_cidade_id 
            ORDER BY id_setor 
            LIMIT 1;
            
            -- Mover jogador
            UPDATE Personagem
            SET nome_planeta = planeta_destino,
                id_setor = primeiro_setor_id
            WHERE id_player = jogador_id;
            
            RETURN 'Viagem realizada com sucesso! Voce chegou em ' || nome_primeira_cidade || 
                   ', setor ' || nome_primeiro_setor || ' no planeta ' || planeta_destino;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para a versão anterior (sem validação de velocidade)
    op.execute("""
        -- Remover função corrigida
        DROP FUNCTION IF EXISTS viajar_para_planeta(INT, VARCHAR(20));
        
        -- Recriar função sem validação de velocidade
        CREATE OR REPLACE FUNCTION viajar_para_planeta(jogador_id INT, planeta_destino VARCHAR(20))
        RETURNS TEXT AS $$
        DECLARE
            nave_jogador VARCHAR(20);
            velocidade_nave INT;
            planeta_atual VARCHAR(20);
            primeira_cidade_id INT;
            nome_primeira_cidade VARCHAR(50);
            primeiro_setor_id INT;
            nome_primeiro_setor VARCHAR(50);
        BEGIN
            -- Verificar se o planeta existe
            IF NOT EXISTS (SELECT 1 FROM Planeta WHERE nome_planeta = planeta_destino) THEN
                RETURN 'Erro: Planeta nao encontrado';
            END IF;
            
            -- Obter dados do jogador
            SELECT nome_planeta, nome_nave INTO planeta_atual, nave_jogador
            FROM Personagem WHERE id_player = jogador_id;
            
            IF planeta_atual = planeta_destino THEN
                RETURN 'Erro: Voce ja esta neste planeta';
            END IF;
            
            -- Verificar se tem nave
            IF nave_jogador IS NULL THEN
                RETURN 'Erro: Voce precisa de uma nave para viajar entre planetas';
            END IF;
            
            -- Verificar velocidade da nave (sem validação de requisitos)
            SELECT velocidade INTO velocidade_nave
            FROM Nave WHERE nome_nave = nave_jogador;
            
            -- Encontrar primeira cidade do planeta destino
            SELECT id_cidade, nome_cidade INTO primeira_cidade_id, nome_primeira_cidade
            FROM Cidade 
            WHERE nome_planeta = planeta_destino 
            ORDER BY id_cidade 
            LIMIT 1;
            
            IF primeira_cidade_id IS NULL THEN
                RETURN 'Erro: Este planeta nao possui cidades disponiveis';
            END IF;
            
            -- Encontrar primeiro setor da primeira cidade
            SELECT id_setor, nome_setor INTO primeiro_setor_id, nome_primeiro_setor
            FROM Setor 
            WHERE id_cidade = primeira_cidade_id 
            ORDER BY id_setor 
            LIMIT 1;
            
            -- Mover jogador
            UPDATE Personagem
            SET nome_planeta = planeta_destino,
                id_setor = primeiro_setor_id
            WHERE id_player = jogador_id;
            
            RETURN 'Viagem realizada com sucesso! Voce chegou em ' || nome_primeira_cidade || 
                   ', setor ' || nome_primeiro_setor || ' no planeta ' || planeta_destino;
        END;
        $$ LANGUAGE plpgsql;
    """)
