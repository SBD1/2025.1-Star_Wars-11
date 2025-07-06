"""Integrar ataques especiais ao sistema de combate

Revision ID: 022
Revises: 021
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '022'
down_revision = '021'
branch_labels = None
depends_on = None

def upgrade():
    # Atualizar função processar_turno_jogador para incluir ataques especiais
    op.execute("""
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20));
        CREATE OR REPLACE FUNCTION processar_turno_jogador(combate_id INT, acao_jogador VARCHAR(20), ataque_especial_id INT DEFAULT NULL)
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
            mana_jogador INT;
            custo_mana INT := 0;
            nome_ataque VARCHAR(50);
            dano_base_ataque INT;
            efeito_especial TEXT;
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

            -- Obter mana atual do jogador
            SELECT mana_atual INTO mana_jogador
            FROM Personagem WHERE id_player = jogador_id;

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

                WHEN 'ataque_especial' THEN
                    -- Verificar se o ataque especial foi fornecido e se o jogador o possui
                    IF ataque_especial_id IS NULL THEN
                        RETURN 'Erro: ID do ataque especial nao fornecido';
                    END IF;
                    
                    SELECT ae.nome_ataque, ae.dano_base, ae.custo_mana, ae.efeito_especial
                    INTO nome_ataque, dano_base_ataque, custo_mana, efeito_especial
                    FROM Ataque_Especial ae
                    INNER JOIN Personagem_Ataque pa ON ae.id_ataque = pa.id_ataque
                    WHERE pa.id_player = jogador_id AND ae.id_ataque = ataque_especial_id;
                    
                    IF NOT FOUND THEN
                        RETURN 'Erro: Voce nao possui este ataque especial';
                    END IF;
                    
                    -- Verificar se tem mana suficiente
                    IF mana_jogador < custo_mana THEN
                        RETURN 'Erro: Mana insuficiente. Necessario: ' || custo_mana || ', Atual: ' || mana_jogador;
                    END IF;
                    
                    -- Calcular dano do ataque especial
                    dano_causado := dano_base_ataque + (calcular_dano(jogador_id, true) / 2);
                    vida_inimigo := vida_inimigo - dano_causado;
                    mana_jogador := mana_jogador - custo_mana;
                    
                    -- Atualizar mana do jogador
                    UPDATE Personagem SET mana_atual = mana_jogador WHERE id_player = jogador_id;
                    
                    IF vida_inimigo <= 0 THEN
                        vida_inimigo := 0;
                        resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano! O inimigo foi derrotado!';
                    ELSE
                        resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano! Inimigo tem ' || vida_inimigo || ' de vida restante.';
                    END IF;
                    
                    -- Adicionar efeito especial à descrição se existir
                    IF efeito_especial IS NOT NULL AND efeito_especial != 'Sempre disponível' THEN
                        resultado_acao := resultado_acao || ' (' || efeito_especial || ')';
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
                    RETURN 'Erro: Acao invalida. Use: ataque, ataque_especial, defesa ou fuga';
            END CASE;

            -- Atualizar vida no combate e mudar turno para inimigo
            UPDATE Combate SET 
                vida_jogador_atual = vida_jogador, 
                vida_inimigo_atual = vida_inimigo,
                turno_atual = 'inimigo'
            WHERE id_combate = combate_id;

            -- Atualizar vida_atual na tabela Personagem
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
    """)
    
    # Função para desbloquear ataques automaticamente ao criar personagem
    op.execute("""
        CREATE OR REPLACE FUNCTION desbloquear_ataques_iniciais(jogador_id INT)
        RETURNS TEXT AS $$
        DECLARE
            classe_jogador VARCHAR(22);
            ataque_inicial_id INT;
        BEGIN
            -- Obter classe do jogador
            SELECT nome_classe INTO classe_jogador
            FROM Personagem WHERE id_player = jogador_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Jogador não encontrado';
            END IF;
            
            -- Desbloquear ataque básico da classe (nível 1)
            SELECT id_ataque INTO ataque_inicial_id
            FROM Ataque_Especial 
            WHERE nome_classe = classe_jogador AND nivel_requerido = 1
            LIMIT 1;
            
            IF FOUND THEN
                INSERT INTO Personagem_Ataque (id_player, id_ataque, nivel_desbloqueio)
                VALUES (jogador_id, ataque_inicial_id, 1)
                ON CONFLICT (id_player, id_ataque) DO NOTHING;
                
                RETURN 'Ataque inicial desbloqueado!';
            ELSE
                RETURN 'Nenhum ataque inicial encontrado para a classe';
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)

def downgrade():
    # Reverter função processar_turno_jogador para versão anterior
    op.execute("""
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20), INT);
        DROP FUNCTION IF EXISTS desbloquear_ataques_iniciais(INT);
        
        -- Recriar versão anterior da função
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
                turno_atual = 'inimigo'
            WHERE id_combate = combate_id;

            -- Atualizar vida_atual na tabela Personagem
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
    """)
