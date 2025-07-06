"""Adicionar vida_atual e xp_atual na tabela Personagem

Revision ID: 019
Revises: 018
Create Date: 2025-07-06

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '019'
down_revision = '018'
branch_labels = None
depends_on = None

def upgrade():
    # Adicionar colunas vida_atual e xp_atual na tabela Personagem
    op.add_column('personagem', sa.Column('vida_atual', sa.Integer(), nullable=False, server_default='100'))
    op.add_column('personagem', sa.Column('xp_atual', sa.Integer(), nullable=False, server_default='0'))

    # Inicializar vida_atual com vida_base e xp_atual com xp para jogadores existentes
    op.execute("""
        UPDATE Personagem
        SET vida_atual = vida_base, xp_atual = xp
        WHERE vida_atual IS NULL OR xp_atual IS NULL;
    """)

    # Corrigir funções de combate para usar vida_atual
    op.execute("""
        -- Corrigir função processar_turno_jogador para atualizar vida na tabela Personagem
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20));
        CREATE OR REPLACE FUNCTION processar_turno_jogador(combate_id INT, acao_jogador VARCHAR(20))
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            vida_jogador INT;
            vida_inimigo INT;
            dano_causado INT := 0;
            resultado_acao TEXT;
            proximo_turno INT;
            status_atual VARCHAR(20);
        BEGIN
            -- Verificar se o combate existe e esta ativo
            SELECT id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate
            INTO jogador_id, inimigo_id, vida_jogador, vida_inimigo, status_atual
            FROM Combate WHERE id_combate = combate_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Combate nao encontrado';
            END IF;

            IF status_atual != 'ativo' THEN
                RETURN 'Erro: Combate nao esta ativo';
            END IF;

            -- Obter proximo numero do turno
            SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno
            FROM Combate_Log WHERE id_combate = combate_id;

            -- Processar acao do jogador
            CASE acao_jogador
                WHEN 'ataque' THEN
                    dano_causado := calcular_dano(jogador_id, true);
                    vida_inimigo := vida_inimigo - dano_causado;
                    
                    IF vida_inimigo <= 0 THEN
                        vida_inimigo := 0;
                        resultado_acao := 'Voce atacou causando ' || dano_causado || ' de dano. O inimigo foi derrotado!';
                    ELSE
                        resultado_acao := 'Voce atacou causando ' || dano_causado || ' de dano. Inimigo tem ' || vida_inimigo || ' de vida restante.';
                    END IF;

                WHEN 'defesa' THEN
                    dano_causado := 0;
                    resultado_acao := 'Voce se defendeu, reduzindo o dano do proximo ataque inimigo.';

                WHEN 'fuga' THEN
                    -- 70% chance de sucesso na fuga
                    IF random() < 0.7 THEN
                        UPDATE Combate 
                        SET status_combate = 'fugiu', data_fim = CURRENT_TIMESTAMP
                        WHERE id_combate = combate_id;

                        resultado_acao := 'Voce fugiu do combate com sucesso!';
                    ELSE
                        resultado_acao := 'Tentativa de fuga falhou! O inimigo te alcancou.';
                    END IF;

                ELSE
                    RETURN 'Erro: Acao invalida. Use: ataque, defesa ou fuga';
            END CASE;

            -- Atualizar vida no combate e mudar turno para inimigo
            UPDATE Combate SET 
                vida_jogador_atual = vida_jogador, 
                vida_inimigo_atual = vida_inimigo,
                turno_atual = 'inimigo'  -- Próximo turno é do inimigo
            WHERE id_combate = combate_id;

            -- NOVO: Atualizar vida_atual na tabela Personagem
            UPDATE Personagem
            SET vida_atual = vida_jogador
            WHERE id_player = jogador_id;

            -- Registrar acao no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, proximo_turno, 'jogador', acao_jogador, dano_causado,
                    vida_jogador, vida_inimigo, resultado_acao);

            -- Verificar se inimigo foi derrotado
            IF vida_inimigo <= 0 THEN
                PERFORM finalizar_combate(combate_id, 'jogador');
            END IF;

            RETURN resultado_acao;
        END;
        $$ LANGUAGE plpgsql;

        -- Corrigir função processar_turno_inimigo para usar vida_atual
        DROP FUNCTION IF EXISTS processar_turno_inimigo(INT);
        CREATE OR REPLACE FUNCTION processar_turno_inimigo(combate_id INT)
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            vida_jogador INT;
            vida_inimigo INT;
            dano_causado INT := 0;
            resultado_acao TEXT;
            proximo_turno_inimigo INT;
            ultima_acao_jogador VARCHAR(20);
            acao_inimigo VARCHAR(20);
            chance_acao INT;
        BEGIN
            -- Verificar se o combate existe e esta ativo
            SELECT id_player, id_mob, vida_jogador_atual, vida_inimigo_atual
            INTO jogador_id, inimigo_id, vida_jogador, vida_inimigo
            FROM Combate WHERE id_combate = combate_id AND status_combate = 'ativo';

            IF NOT FOUND THEN
                RETURN 'Erro: Combate nao encontrado ou nao esta ativo';
            END IF;

            -- Obter proximo numero do turno para o inimigo
            SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno_inimigo
            FROM Combate_Log WHERE id_combate = combate_id;

            -- Obter ultima acao do jogador para IA simples
            SELECT acao INTO ultima_acao_jogador
            FROM Combate_Log
            WHERE id_combate = combate_id AND ator = 'jogador'
            ORDER BY turno_numero DESC LIMIT 1;

            -- IA simples: 80% ataque, 20% defesa (mais se jogador defendeu)
            chance_acao := (random() * 100)::INT;

            IF ultima_acao_jogador = 'defesa' AND chance_acao <= 40 THEN
                acao_inimigo := 'defesa';
            ELSIF chance_acao <= 80 THEN
                acao_inimigo := 'ataque';
            ELSE
                acao_inimigo := 'defesa';
            END IF;

            -- Processar acao do inimigo
            CASE acao_inimigo
                WHEN 'ataque' THEN
                    dano_causado := calcular_dano(inimigo_id, false);

                    -- Reduzir dano se jogador defendeu no turno anterior
                    IF ultima_acao_jogador = 'defesa' THEN
                        dano_causado := GREATEST(1, dano_causado / 2);
                    END IF;

                    vida_jogador := vida_jogador - dano_causado;

                    IF vida_jogador <= 0 THEN
                        vida_jogador := 0;
                        resultado_acao := 'O inimigo atacou causando ' || dano_causado || ' de dano! Voce foi derrotado!';
                    ELSE
                        resultado_acao := 'O inimigo atacou causando ' || dano_causado || ' de dano!';
                    END IF;

                WHEN 'defesa' THEN
                    dano_causado := 0;
                    resultado_acao := 'O inimigo se defendeu, preparando-se para o proximo ataque.';

                ELSE
                    resultado_acao := 'O inimigo hesitou...';
            END CASE;

            -- Atualizar vida no combate e mudar turno para jogador
            UPDATE Combate SET
                vida_jogador_atual = vida_jogador,
                vida_inimigo_atual = vida_inimigo,
                turno_atual = 'jogador'
            WHERE id_combate = combate_id;

            -- Atualizar vida_atual na tabela Personagem
            UPDATE Personagem
            SET vida_atual = vida_jogador
            WHERE id_player = jogador_id;

            -- Registrar acao no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, proximo_turno_inimigo, 'inimigo', acao_inimigo, dano_causado,
                    vida_jogador, vida_inimigo, resultado_acao);

            -- Verificar se jogador foi derrotado
            IF vida_jogador <= 0 THEN
                PERFORM finalizar_combate(combate_id, 'inimigo');
            END IF;

            RETURN resultado_acao;
        END;
        $$ LANGUAGE plpgsql;

        -- Corrigir função iniciar_combate para usar vida_atual
        DROP FUNCTION IF EXISTS iniciar_combate(INT, INT);
        CREATE OR REPLACE FUNCTION iniciar_combate(jogador_id INT, inimigo_id INT)
        RETURNS TEXT AS $$
        DECLARE
            vida_jogador_atual INT;
            vida_inimigo_base INT;
            combate_id INT;
        BEGIN
            -- Verificar se jogador já está em combate
            IF EXISTS (SELECT 1 FROM Combate WHERE id_player = jogador_id AND status_combate = 'ativo') THEN
                RETURN 'Erro: Voce ja esta em combate!';
            END IF;

            -- Obter vida atual do jogador
            SELECT vida_atual INTO vida_jogador_atual
            FROM Personagem WHERE id_player = jogador_id;

            -- Obter vida base do inimigo
            SELECT vida_base INTO vida_inimigo_base
            FROM Inimigo WHERE id_mob = inimigo_id;

            -- Criar novo combate
            INSERT INTO Combate (id_player, id_mob, vida_jogador_atual, vida_inimigo_atual,
                               turno_atual, status_combate, data_inicio)
            VALUES (jogador_id, inimigo_id, vida_jogador_atual, vida_inimigo_base,
                   'jogador', 'ativo', CURRENT_TIMESTAMP)
            RETURNING id_combate INTO combate_id;

            RETURN 'Combate iniciado! ID: ' || combate_id;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Remover colunas vida_atual e xp_atual
    op.drop_column('personagem', 'vida_atual')
    op.drop_column('personagem', 'xp_atual')

    # Reverter funções para versão anterior
    op.execute("""
        -- Reverter função processar_turno_jogador sem sincronização de vida
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20));
        CREATE OR REPLACE FUNCTION processar_turno_jogador(combate_id INT, acao_jogador VARCHAR(20))
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            vida_jogador INT;
            vida_inimigo INT;
            dano_causado INT := 0;
            resultado_acao TEXT;
            proximo_turno INT;
            status_atual VARCHAR(20);
        BEGIN
            -- Verificar se o combate existe e esta ativo
            SELECT id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate
            INTO jogador_id, inimigo_id, vida_jogador, vida_inimigo, status_atual
            FROM Combate WHERE id_combate = combate_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Combate nao encontrado';
            END IF;

            IF status_atual != 'ativo' THEN
                RETURN 'Erro: Combate nao esta ativo';
            END IF;

            -- Obter proximo numero do turno
            SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno
            FROM Combate_Log WHERE id_combate = combate_id;

            -- Processar acao do jogador
            CASE acao_jogador
                WHEN 'ataque' THEN
                    dano_causado := calcular_dano(jogador_id, true);
                    vida_inimigo := vida_inimigo - dano_causado;
                    
                    IF vida_inimigo <= 0 THEN
                        vida_inimigo := 0;
                        resultado_acao := 'Voce atacou causando ' || dano_causado || ' de dano. O inimigo foi derrotado!';
                    ELSE
                        resultado_acao := 'Voce atacou causando ' || dano_causado || ' de dano. Inimigo tem ' || vida_inimigo || ' de vida restante.';
                    END IF;

                WHEN 'defesa' THEN
                    dano_causado := 0;
                    resultado_acao := 'Voce se defendeu, reduzindo o dano do proximo ataque inimigo.';

                WHEN 'fuga' THEN
                    -- 70% chance de sucesso na fuga
                    IF random() < 0.7 THEN
                        UPDATE Combate 
                        SET status_combate = 'fugiu', data_fim = CURRENT_TIMESTAMP
                        WHERE id_combate = combate_id;

                        resultado_acao := 'Voce fugiu do combate com sucesso!';
                    ELSE
                        resultado_acao := 'Tentativa de fuga falhou! O inimigo te alcancou.';
                    END IF;

                ELSE
                    RETURN 'Erro: Acao invalida. Use: ataque, defesa ou fuga';
            END CASE;

            -- Atualizar vida no combate e mudar turno para inimigo (SEM sincronizar com Personagem)
            UPDATE Combate SET 
                vida_jogador_atual = vida_jogador, 
                vida_inimigo_atual = vida_inimigo,
                turno_atual = 'inimigo'  -- Próximo turno é do inimigo
            WHERE id_combate = combate_id;

            -- Registrar acao no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, proximo_turno, 'jogador', acao_jogador, dano_causado,
                    vida_jogador, vida_inimigo, resultado_acao);

            -- Verificar se inimigo foi derrotado
            IF vida_inimigo <= 0 THEN
                PERFORM finalizar_combate(combate_id, 'jogador');
            END IF;

            RETURN resultado_acao;
        END;
        $$ LANGUAGE plpgsql;
    """)
