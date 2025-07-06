"""Corrigir ataques especiais conforme MER - 3 habilidades por classe

Revision ID: 024
Revises: 023
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '024'
down_revision = '023'
branch_labels = None
depends_on = None

def upgrade():
    # Limpar ataques existentes e implementar conforme MER
    op.execute("""
        -- Limpar ataques existentes
        DELETE FROM Personagem_Ataque;
        DELETE FROM Ataque_Especial;
        
        -- ATAQUES JEDI (conforme MER)
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Lightsaber Strike', 'Ataque básico com sabre de luz', 25, 0, 1, 'Jedi', 'fisico', 'Ataque básico sempre disponível'),
        ('Force Push', 'Empurra o inimigo usando a Força', 20, 15, 3, 'Jedi', 'forca', 'Pode atordoar o inimigo por 1 turno'),
        ('Force Heal', 'Cura ferimentos usando a Força', 0, 20, 5, 'Jedi', 'forca', 'Restaura 40 pontos de vida');
        
        -- ATAQUES SITH (conforme MER)
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Dark Strike', 'Ataque sombrio com sabre vermelho', 25, 0, 1, 'Sith', 'fisico', 'Ataque básico sempre disponível'),
        ('Force Lightning', 'Dispara raios de energia sombria', 35, 18, 3, 'Sith', 'forca', 'Pode causar paralisia temporária'),
        ('Force Drain', 'Drena a energia vital do inimigo', 25, 22, 5, 'Sith', 'forca', 'Absorve 50% do dano como vida');
        
        -- ATAQUES CAÇADOR DE RECOMPENSAS (conforme MER)
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Precise Shot', 'Tiro certeiro com blaster', 22, 0, 1, 'Cacador_de_Recompensas', 'tecnologico', 'Ataque básico sempre disponível'),
        ('Explosive Grenade', 'Granada explosiva de alto impacto', 30, 16, 3, 'Cacador_de_Recompensas', 'tecnologico', 'Dano em área, pode atordoar'),
        ('Rapid Fire', 'Rajada rápida de múltiplos disparos', 40, 25, 5, 'Cacador_de_Recompensas', 'tecnologico', 'Múltiplos ataques em sequência');
    """)
    
    # Atualizar função para implementar efeito de cura do Force Heal
    op.execute("""
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20), INT);
        CREATE OR REPLACE FUNCTION processar_turno_jogador(combate_id INT, acao_jogador VARCHAR(20), ataque_especial_id INT DEFAULT NULL)
        RETURNS TEXT AS $$
        DECLARE
            jogador_id INT;
            inimigo_id INT;
            vida_jogador INT;
            vida_inimigo INT;
            vida_maxima_jogador INT;
            dano_causado INT := 0;
            cura_realizada INT := 0;
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

            -- Obter mana atual e vida máxima do jogador
            SELECT mana_atual, vida_base INTO mana_jogador, vida_maxima_jogador
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
                    
                    -- Processar ataque especial
                    IF nome_ataque = 'Force Heal' THEN
                        -- Force Heal: cura em vez de causar dano
                        cura_realizada := 40;
                        vida_jogador := LEAST(vida_jogador + cura_realizada, vida_maxima_jogador);
                        mana_jogador := mana_jogador - custo_mana;
                        
                        resultado_acao := 'Voce usou ' || nome_ataque || ' e recuperou ' || cura_realizada || ' pontos de vida!';
                    ELSIF nome_ataque = 'Force Drain' THEN
                        -- Force Drain: causa dano e cura o jogador
                        dano_causado := dano_base_ataque + (calcular_dano(jogador_id, true) / 2);
                        vida_inimigo := vida_inimigo - dano_causado;
                        cura_realizada := dano_causado / 2;
                        vida_jogador := LEAST(vida_jogador + cura_realizada, vida_maxima_jogador);
                        mana_jogador := mana_jogador - custo_mana;
                        
                        IF vida_inimigo <= 0 THEN
                            vida_inimigo := 0;
                            resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano e absorveu ' || cura_realizada || ' de vida! O inimigo foi derrotado!';
                        ELSE
                            resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano e absorveu ' || cura_realizada || ' de vida! Inimigo tem ' || vida_inimigo || ' de vida restante.';
                        END IF;
                    ELSE
                        -- Ataques normais que causam dano
                        dano_causado := dano_base_ataque + (calcular_dano(jogador_id, true) / 2);
                        vida_inimigo := vida_inimigo - dano_causado;
                        mana_jogador := mana_jogador - custo_mana;
                        
                        IF vida_inimigo <= 0 THEN
                            vida_inimigo := 0;
                            resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano! O inimigo foi derrotado!';
                        ELSE
                            resultado_acao := 'Voce usou ' || nome_ataque || ' causando ' || dano_causado || ' de dano! Inimigo tem ' || vida_inimigo || ' de vida restante.';
                        END IF;
                    END IF;
                    
                    -- Atualizar mana do jogador
                    UPDATE Personagem SET mana_atual = mana_jogador WHERE id_player = jogador_id;

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

def downgrade():
    # Reverter para ataques anteriores
    op.execute("""
        DELETE FROM Personagem_Ataque;
        DELETE FROM Ataque_Especial;
        
        -- Restaurar ataques anteriores (versão original)
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Golpe de Sabre', 'Ataque básico com sabre de luz', 25, 0, 1, 'Jedi', 'fisico', 'Sempre disponível'),
        ('Empurrão da Força', 'Empurra o inimigo causando dano', 20, 10, 3, 'Jedi', 'forca', 'Pode atordoar por 1 turno'),
        ('Cura da Força', 'Restaura vida usando a Força', 0, 15, 5, 'Jedi', 'forca', 'Cura 30 pontos de vida'),
        ('Golpe Sombrio', 'Ataque básico com sabre vermelho', 25, 0, 1, 'Sith', 'fisico', 'Sempre disponível'),
        ('Raio da Força', 'Dispara raios de energia sombria', 30, 12, 3, 'Sith', 'forca', 'Pode causar paralisia'),
        ('Drenar Vida', 'Absorve vida do inimigo', 20, 15, 5, 'Sith', 'forca', 'Cura 50% do dano causado'),
        ('Tiro Certeiro', 'Disparo básico com blaster', 22, 0, 1, 'Cacador_de_Recompensas', 'tecnologico', 'Sempre disponível'),
        ('Granada Atordoante', 'Granada que causa dano e atordoa', 25, 8, 3, 'Cacador_de_Recompensas', 'tecnologico', 'Atordoa por 2 turnos'),
        ('Tiro Duplo', 'Dois disparos rápidos', 35, 12, 5, 'Cacador_de_Recompensas', 'tecnologico', 'Dois ataques em sequência');
    """)
