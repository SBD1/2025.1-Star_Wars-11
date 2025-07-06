"""Corrigir função obter_status_combate para retornar turno_atual correto

Revision ID: 015
Revises: 014
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '015'
down_revision = '014'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir a função obter_status_combate e as funções de processamento de turno
    op.execute("""
        -- Remover função existente
        DROP FUNCTION IF EXISTS obter_status_combate(integer);

        -- Recriar função corrigida
        CREATE OR REPLACE FUNCTION obter_status_combate(jogador_id INT)
        RETURNS TABLE (
            id_combate INT,
            tipo_inimigo VARCHAR(22),
            vida_jogador INT,
            vida_inimigo INT,
            turno_atual VARCHAR(10),
            turno_numero INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT
                c.id_combate,
                i.tipo_mob,
                c.vida_jogador_atual,
                c.vida_inimigo_atual,
                c.turno_atual,  -- Retorna 'jogador' ou 'inimigo'
                COALESCE(MAX(cl.turno_numero), 0) as turno_numero
            FROM Combate c
            JOIN Inimigo i ON c.id_mob = i.id_mob
            LEFT JOIN Combate_Log cl ON c.id_combate = cl.id_combate
            WHERE c.id_player = jogador_id AND c.status_combate = 'ativo'
            GROUP BY c.id_combate, i.tipo_mob, c.vida_jogador_atual, c.vida_inimigo_atual, c.turno_atual;
        END;
        $$ LANGUAGE plpgsql;

        -- Corrigir função processar_turno_jogador para atualizar turno_atual
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

        -- Corrigir função processar_turno_inimigo para atualizar turno_atual
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
                turno_atual = 'jogador'  -- Próximo turno é do jogador
            WHERE id_combate = combate_id;

            -- Registrar acao no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, proximo_turno_inimigo, 'inimigo', acao_inimigo, dano_causado,
                    vida_jogador, vida_inimigo, resultado_acao);

            -- Verificar se jogador foi derrotado
            IF vida_jogador <= 0 THEN
                PERFORM finalizar_combate(combate_id, 'inimigo');
                resultado_acao := resultado_acao || ' Voce foi derrotado!';
            END IF;

            RETURN resultado_acao;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter para a versão anterior (com problema)
    op.execute("""
        -- Remover função corrigida
        DROP FUNCTION IF EXISTS obter_status_combate(integer);
        
        -- Recriar função com problema
        CREATE OR REPLACE FUNCTION obter_status_combate(jogador_id INT)
        RETURNS TABLE (
            id_combate INT,
            tipo_inimigo VARCHAR(22),
            vida_jogador INT,
            vida_inimigo INT,
            status_combate VARCHAR(20),
            turno_atual INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT
                c.id_combate,
                i.tipo_mob,
                c.vida_jogador_atual,
                c.vida_inimigo_atual,
                c.status_combate,
                COALESCE(MAX(cl.turno_numero), 0) as turno_atual
            FROM Combate c
            JOIN Inimigo i ON c.id_mob = i.id_mob
            LEFT JOIN Combate_Log cl ON c.id_combate = cl.id_combate
            WHERE c.id_player = jogador_id AND c.status_combate = 'ativo'
            GROUP BY c.id_combate, i.tipo_mob, c.vida_jogador_atual, c.vida_inimigo_atual, c.status_combate;
        END;
        $$ LANGUAGE plpgsql;
    """)
