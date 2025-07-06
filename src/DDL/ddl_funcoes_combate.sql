-- =====================================================
-- Procedures Sistema de Combate - Star Wars MUD
-- =====================================================

-- Funcao para listar inimigos disponiveis no planeta do jogador
CREATE OR REPLACE FUNCTION listar_inimigos_planeta(jogador_id INT)
RETURNS TABLE (
    id_mob INT,
    tipo_mob VARCHAR(22),
    vida_base INT,
    nivel INT,
    dano_base INT,
    pontos_escudo INT,
    creditos INT,
    nivel_ameaca INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id_mob,
        i.tipo_mob,
        i.vida_base,
        i.nivel,
        i.dano_base,
        i.pontos_escudo,
        i.creditos,
        m.nivel_ameaca
    FROM Inimigo i
    JOIN MOB m ON i.tipo_mob = m.tipo_mob
    JOIN Personagem p ON p.nome_planeta = i.planeta_origem
    WHERE p.id_player = jogador_id
    ORDER BY m.nivel_ameaca, i.nivel;
END;
$$ LANGUAGE plpgsql;

-- Funcao para iniciar um combate
CREATE OR REPLACE FUNCTION iniciar_combate(jogador_id INT, inimigo_id INT)
RETURNS TEXT AS $$
DECLARE
    jogador_vida INT;
    inimigo_vida INT;
    jogador_setor INT;
    combate_id INT;
    inimigo_nome VARCHAR(22);
    inimigo_no_setor BOOLEAN := FALSE;
BEGIN
    -- Verificar se o jogador existe e obter dados
    SELECT vida_base, id_setor INTO jogador_vida, jogador_setor
    FROM Personagem WHERE id_player = jogador_id;

    IF NOT FOUND THEN
        RETURN 'Erro: Jogador nao encontrado';
    END IF;

    -- Verificar se o inimigo existe e obter dados
    SELECT vida_base, tipo_mob INTO inimigo_vida, inimigo_nome
    FROM Inimigo WHERE id_mob = inimigo_id;

    IF NOT FOUND THEN
        RETURN 'Erro: Inimigo nao encontrado';
    END IF;

    -- Verificar se o inimigo esta no setor atual do jogador
    SELECT EXISTS(
        SELECT 1 FROM Inimigo_Setor
        WHERE id_setor = jogador_setor AND id_mob = inimigo_id AND ativo = true
    ) INTO inimigo_no_setor;

    IF NOT inimigo_no_setor THEN
        RETURN 'Erro: Voce nao pode lutar contra este inimigo. Ele nao esta no seu setor atual';
    END IF;
    
    -- Verificar se o jogador ja esta em combate
    SELECT id_combate INTO combate_id
    FROM Combate 
    WHERE id_player = jogador_id AND status_combate = 'ativo';
    
    IF FOUND THEN
        RETURN 'Erro: Voce ja esta em combate. Finalize o combate atual primeiro';
    END IF;
    
    -- Criar novo combate
    INSERT INTO Combate (id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate)
    VALUES (jogador_id, inimigo_id, jogador_vida, inimigo_vida, 'ativo')
    RETURNING id_combate INTO combate_id;
    
    -- Registrar inicio do combate no log
    INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado, 
                            vida_restante_jogador, vida_restante_inimigo, descricao_acao)
    VALUES (combate_id, 0, 'sistema', 'inicio', 0, jogador_vida, inimigo_vida, 
            'Combate iniciado contra ' || inimigo_nome);
    
    RETURN 'Combate iniciado contra ' || inimigo_nome || '! Use os comandos de combate para lutar.';
END;
$$ LANGUAGE plpgsql;

-- Funcao para calcular dano baseado em level e classe
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
    
    -- Variacao aleatoria de ±20%
    dano_final := dano_final + floor((random() * 0.4 - 0.2) * dano_final);
    
    -- Garantir dano minimo
    IF dano_final < 1 THEN
        dano_final := 1;
    END IF;
    
    RETURN dano_final;
END;
$$ LANGUAGE plpgsql;

-- Funcao para processar turno do jogador
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

    -- Atualizar vida no combate
    UPDATE Combate SET vida_jogador_atual = vida_jogador, vida_inimigo_atual = vida_inimigo
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

-- Funcao para processar turno do inimigo (IA simples)
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

    -- Obter proximo numero do turno
    SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno_inimigo
    FROM Combate_Log WHERE id_combate = combate_id;

    -- Obter ultima acao do jogador para IA
    SELECT acao INTO ultima_acao_jogador
    FROM Combate_Log
    WHERE id_combate = combate_id AND ator = 'jogador'
    ORDER BY turno_numero DESC LIMIT 1;

    -- IA simples do inimigo
    IF ultima_acao_jogador = 'defesa' THEN
        -- Se jogador se defendeu, inimigo ataca com forca
        acao_inimigo := 'ataque';
        dano_causado := calcular_dano(inimigo_id, false);
        vida_jogador := vida_jogador - dano_causado;
        resultado_acao := 'O inimigo aproveitou sua defesa e atacou com forca, causando ' || dano_causado || ' de dano!';
    ELSE
        -- 80% chance de atacar, 20% de defender
        chance_acao := floor(random() * 100) + 1;

        IF chance_acao <= 80 THEN
            acao_inimigo := 'ataque';
            dano_causado := calcular_dano(inimigo_id, false);

            -- Reduzir dano se jogador se defendeu no turno anterior
            IF ultima_acao_jogador = 'defesa' THEN
                dano_causado := dano_causado / 2;
            END IF;

            vida_jogador := vida_jogador - dano_causado;
            resultado_acao := 'O inimigo atacou causando ' || dano_causado || ' de dano!';
        ELSE
            acao_inimigo := 'defesa';
            dano_causado := 0;
            resultado_acao := 'O inimigo se defendeu, preparando-se para o proximo turno.';
        END IF;
    END IF;

    -- Garantir que vida nao fique negativa
    IF vida_jogador < 0 THEN
        vida_jogador := 0;
    END IF;

    -- Atualizar vida no combate
    UPDATE Combate SET vida_jogador_atual = vida_jogador, vida_inimigo_atual = vida_inimigo
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

-- Funcao para finalizar combate e distribuir recompensas
CREATE OR REPLACE FUNCTION finalizar_combate(combate_id INT, vencedor VARCHAR(10))
RETURNS TEXT AS $$
DECLARE
    jogador_id INT;
    inimigo_id INT;
    jogador_level_atual INT;
    novo_level INT;
    xp_recompensa INT;
    gcs_recompensa INT;
    nivel_inimigo INT;
    creditos_inimigo INT;
    resultado_texto TEXT;
    data_inicio_combate TIMESTAMP;
    duracao INTERVAL;
    total_turnos INT;
    dano_total_jogador INT;
    dano_total_inimigo INT;
    vida_ressurreicao INT;
    gcs_atual INT;
BEGIN
    -- Obter dados do combate
    SELECT id_player, id_mob, data_inicio INTO jogador_id, inimigo_id, data_inicio_combate
    FROM Combate WHERE id_combate = combate_id;

    IF NOT FOUND THEN
        RETURN 'Erro: Combate nao encontrado';
    END IF;

    -- Calcular duracao
    duracao := CURRENT_TIMESTAMP - data_inicio_combate;

    -- Obter estatisticas do combate
    SELECT COUNT(*),
           COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
           COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
    INTO total_turnos, dano_total_jogador, dano_total_inimigo
    FROM Combate_Log WHERE id_combate = combate_id;

    IF vencedor = 'jogador' THEN
        -- Obter dados do inimigo para calcular recompensas
        SELECT nivel, creditos INTO nivel_inimigo, creditos_inimigo
        FROM Inimigo WHERE id_mob = inimigo_id;

        -- XP baseado no nivel do inimigo
        xp_recompensa := nivel_inimigo * 50 + 25;

        -- GCS baseado nos creditos do inimigo
        gcs_recompensa := creditos_inimigo;

        -- Obter level atual do jogador
        SELECT level INTO jogador_level_atual FROM Personagem WHERE id_player = jogador_id;

        -- Calcular novo level baseado no XP
        novo_level := LEAST(floor((xp_recompensa + (SELECT xp FROM Personagem WHERE id_player = jogador_id)) / 100.0) + 1, 50);

        -- Atualizar jogador com recompensas
        UPDATE Personagem
        SET xp = xp + xp_recompensa,
            gcs = gcs + gcs_recompensa,
            level = novo_level,
            vitorias = vitorias + 1,
            vida_base = 100  -- Restaurar vida apos vitoria
        WHERE id_player = jogador_id;

        resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

        IF novo_level > jogador_level_atual THEN
            resultado_texto := resultado_texto || ' Parabens! Voce subiu para o level ' || novo_level || '!';
        END IF;

    ELSIF vencedor = 'inimigo' THEN
        -- Jogador foi derrotado
        SELECT level, gcs INTO jogador_level_atual, gcs_atual FROM Personagem WHERE id_player = jogador_id;

        -- Determinar vida de ressurreicao baseada nos GCS
        IF gcs_atual >= 100 THEN
            vida_ressurreicao := 100;  -- Vida completa se tiver dinheiro
        ELSE
            vida_ressurreicao := 50;   -- Vida reduzida se nao tiver dinheiro
        END IF;

        -- Aplicar penalidades por morte
        UPDATE Personagem
        SET mortes = mortes + 1,
            gcs = GREATEST(gcs - 100, 0),  -- Perde 100 GCS (minimo 0)
            xp = GREATEST(xp - (level * 10), 0),  -- Perde XP baseado no level
            vida_base = vida_ressurreicao  -- Vida baseada nos GCS disponiveis
        WHERE id_player = jogador_id;

        -- Mensagem personalizada baseada na situacao
        IF gcs_atual >= 100 THEN
            resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.';
        ELSE
            resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).';
        END IF;
    ELSE
        -- Fuga - apenas restaurar vida
        UPDATE Personagem
        SET vida_base = 100
        WHERE id_player = jogador_id;

        resultado_texto := 'Voce fugiu do combate.';
    END IF;

    -- Finalizar combate
    UPDATE Combate
    SET status_combate = CASE
                            WHEN vencedor = 'jogador' THEN 'vitoria'
                            WHEN vencedor = 'inimigo' THEN 'derrota'
                            ELSE 'fugiu'
                        END,
        data_fim = CURRENT_TIMESTAMP
    WHERE id_combate = combate_id;

    RETURN resultado_texto;
END;
$$ LANGUAGE plpgsql;

-- Funcao para obter status do combate atual do jogador
DROP FUNCTION IF EXISTS obter_status_combate(integer);
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
