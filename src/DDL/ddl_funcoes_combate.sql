-- =====================================================
-- Procedures Sistema de Combate - Star Wars MUD
-- =====================================================

-- Função para listar inimigos disponíveis no planeta do jogador
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

-- Função para iniciar um combate
CREATE OR REPLACE FUNCTION iniciar_combate(jogador_id INT, inimigo_id INT)
RETURNS TEXT AS $$
DECLARE
    jogador_vida INT;
    inimigo_vida INT;
    inimigo_planeta VARCHAR(20);
    jogador_planeta VARCHAR(20);
    combate_id INT;
    inimigo_nome VARCHAR(22);
BEGIN
    -- Verificar se o jogador existe e obter dados
    SELECT vida_base, nome_planeta INTO jogador_vida, jogador_planeta
    FROM Personagem WHERE id_player = jogador_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Jogador não encontrado';
    END IF;
    
    -- Verificar se o inimigo existe e obter dados
    SELECT vida_base, planeta_origem, tipo_mob INTO inimigo_vida, inimigo_planeta, inimigo_nome
    FROM Inimigo WHERE id_mob = inimigo_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Inimigo não encontrado';
    END IF;
    
    -- Verificar se jogador e inimigo estão no mesmo planeta
    IF jogador_planeta != inimigo_planeta THEN
        RETURN 'Erro: Você não pode lutar contra este inimigo. Ele não está no seu planeta atual';
    END IF;
    
    -- Verificar se o jogador já está em combate
    SELECT id_combate INTO combate_id
    FROM Combate 
    WHERE id_player = jogador_id AND status_combate = 'ativo';
    
    IF FOUND THEN
        RETURN 'Erro: Você já está em combate. Finalize o combate atual primeiro';
    END IF;
    
    -- Criar novo combate
    INSERT INTO Combate (id_player, id_mob, vida_jogador_atual, vida_inimigo_atual)
    VALUES (jogador_id, inimigo_id, jogador_vida, inimigo_vida)
    RETURNING id_combate INTO combate_id;
    
    -- Registrar início do combate no log
    INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado, 
                            vida_restante_jogador, vida_restante_inimigo, descricao_acao)
    VALUES (combate_id, 0, 'jogador', 'inicio', 0, jogador_vida, inimigo_vida, 
            'Combate iniciado contra ' || inimigo_nome);
    
    RETURN 'Sucesso: Combate iniciado contra ' || inimigo_nome || '! ID do combate: ' || combate_id;
END;
$$ LANGUAGE plpgsql;

-- Função para calcular dano baseado em level e classe
CREATE OR REPLACE FUNCTION calcular_dano(atacante_id INT, eh_jogador BOOLEAN)
RETURNS INT AS $$
DECLARE
    dano_base INT;
    nivel_atacante INT;
    classe_atacante VARCHAR(22);
    modificador_classe INT := 0;
    dano_final INT;
    chance_critico INT;
BEGIN
    IF eh_jogador THEN
        -- Dados do jogador
        SELECT p.dano_base, p.level, p.nome_classe 
        INTO dano_base, nivel_atacante, classe_atacante
        FROM Personagem p WHERE p.id_player = atacante_id;
        
        -- Modificadores por classe
        CASE classe_atacante
            WHEN 'Jedi' THEN modificador_classe := 5;
            WHEN 'Sith' THEN modificador_classe := 8;
            WHEN 'Cacador_de_Recompensas' THEN modificador_classe := 10;
            ELSE modificador_classe := 0;
        END CASE;
    ELSE
        -- Dados do inimigo
        SELECT i.dano_base, i.nivel 
        INTO dano_base, nivel_atacante
        FROM Inimigo i WHERE i.id_mob = atacante_id;
        
        modificador_classe := 0;
    END IF;
    
    -- Cálculo base do dano (balanceado)
    IF eh_jogador THEN
        -- Jogador: dano base + level*3 + modificador classe
        dano_final := dano_base + (nivel_atacante * 3) + modificador_classe;
    ELSE
        -- Inimigo: dano base reduzido + level*1.5 (mais fraco que jogador)
        dano_final := (dano_base * 0.6) + (nivel_atacante * 1.5);
    END IF;
    
    -- Chance de crítico (5%)
    chance_critico := floor(random() * 100) + 1;
    IF chance_critico <= 5 THEN
        dano_final := dano_final * 2;
    END IF;
    
    -- Variação aleatória de ±20%
    dano_final := dano_final + floor((random() * 0.4 - 0.2) * dano_final);
    
    -- Garantir dano mínimo
    IF dano_final < 1 THEN
        dano_final := 1;
    END IF;
    
    RETURN dano_final;
END;
$$ LANGUAGE plpgsql;

-- Função para processar turno do jogador
CREATE OR REPLACE FUNCTION processar_turno_jogador(combate_id INT, acao_jogador VARCHAR(20))
RETURNS TEXT AS $$
DECLARE
    jogador_id INT;
    inimigo_id INT;
    vida_jogador INT;
    vida_inimigo INT;
    proximo_turno INT;
    dano_causado INT;
    resultado_acao TEXT;
    status_atual VARCHAR(20);
BEGIN
    -- Verificar se o combate existe e está ativo
    SELECT id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate
    INTO jogador_id, inimigo_id, vida_jogador, vida_inimigo, status_atual
    FROM Combate WHERE id_combate = combate_id;

    IF NOT FOUND THEN
        RETURN 'Erro: Combate não encontrado';
    END IF;

    IF status_atual != 'ativo' THEN
        RETURN 'Erro: Combate não está ativo';
    END IF;

    -- Obter próximo número do turno
    SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno
    FROM Combate_Log WHERE id_combate = combate_id;

    -- Processar ação do jogador
    CASE acao_jogador
        WHEN 'ataque' THEN
            dano_causado := calcular_dano(jogador_id, true);
            vida_inimigo := vida_inimigo - dano_causado;

            IF vida_inimigo <= 0 THEN
                vida_inimigo := 0;
                resultado_acao := 'Você atacou causando ' || dano_causado || ' de dano. O inimigo foi derrotado!';
            ELSE
                resultado_acao := 'Você atacou causando ' || dano_causado || ' de dano. Inimigo tem ' || vida_inimigo || ' de vida restante.';
            END IF;

        WHEN 'defesa' THEN
            dano_causado := 0;
            resultado_acao := 'Você se defendeu, reduzindo o dano do próximo ataque inimigo.';

        WHEN 'fuga' THEN
            dano_causado := 0;
            -- 70% de chance de fuga bem-sucedida
            IF (floor(random() * 100) + 1) <= 70 THEN
                UPDATE Combate SET status_combate = 'fugiu', data_fim = CURRENT_TIMESTAMP
                WHERE id_combate = combate_id;

                resultado_acao := 'Você fugiu do combate com sucesso!';
            ELSE
                resultado_acao := 'Tentativa de fuga falhou! O inimigo te alcançou.';
            END IF;

        ELSE
            RETURN 'Erro: Ação inválida. Use: ataque, defesa ou fuga';
    END CASE;

    -- Atualizar vida do inimigo no combate
    UPDATE Combate SET vida_inimigo_atual = vida_inimigo, turno_atual = 'inimigo'
    WHERE id_combate = combate_id;

    -- Registrar ação no log
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

-- Função para processar turno do inimigo (IA simples)
CREATE OR REPLACE FUNCTION processar_turno_inimigo(combate_id INT)
RETURNS TEXT AS $$
DECLARE
    jogador_id INT;
    inimigo_id INT;
    vida_jogador INT;
    vida_inimigo INT;
    proximo_turno_inimigo INT;
    dano_causado INT;
    resultado_acao TEXT;
    acao_inimigo VARCHAR(20);
    ultima_acao_jogador VARCHAR(20);
BEGIN
    -- Obter dados do combate
    SELECT id_player, id_mob, vida_jogador_atual, vida_inimigo_atual
    INTO jogador_id, inimigo_id, vida_jogador, vida_inimigo
    FROM Combate WHERE id_combate = combate_id AND status_combate = 'ativo';

    IF NOT FOUND THEN
        RETURN 'Erro: Combate não encontrado ou não está ativo';
    END IF;

    -- Obter próximo número do turno
    SELECT COALESCE(MAX(turno_numero), 0) + 1 INTO proximo_turno_inimigo
    FROM Combate_Log WHERE id_combate = combate_id;

    -- Obter última ação do jogador para IA
    SELECT acao INTO ultima_acao_jogador
    FROM Combate_Log
    WHERE id_combate = combate_id AND ator = 'jogador'
    ORDER BY turno_numero DESC LIMIT 1;

    -- IA simples do inimigo
    IF ultima_acao_jogador = 'defesa' THEN
        -- Se jogador se defendeu, inimigo ataca com força
        acao_inimigo := 'ataque';
        dano_causado := calcular_dano(inimigo_id, false);
        vida_jogador := vida_jogador - dano_causado;
        resultado_acao := 'O inimigo aproveitou sua defesa e atacou com força, causando ' || dano_causado || ' de dano!';
    ELSE
        -- 80% chance de atacar, 20% de defender
        IF (floor(random() * 100) + 1) <= 80 THEN
            acao_inimigo := 'ataque';
            dano_causado := calcular_dano(inimigo_id, false);
            -- Se jogador se defendeu no turno anterior, reduz dano em 50%
            IF ultima_acao_jogador = 'defesa' THEN
                dano_causado := dano_causado / 2;
                resultado_acao := 'O inimigo atacou, mas sua defesa reduziu o dano para ' || dano_causado || '!';
            ELSE
                resultado_acao := 'O inimigo atacou causando ' || dano_causado || ' de dano!';
            END IF;
            vida_jogador := vida_jogador - dano_causado;
        ELSE
            acao_inimigo := 'defesa';
            dano_causado := 0;
            resultado_acao := 'O inimigo se defendeu, preparando-se para o próximo turno.';
        END IF;
    END IF;

    -- Garantir que vida não fique negativa
    IF vida_jogador < 0 THEN
        vida_jogador := 0;
    END IF;

    -- Atualizar vida do jogador no combate
    UPDATE Combate SET vida_jogador_atual = vida_jogador, turno_atual = 'jogador'
    WHERE id_combate = combate_id;

    -- Registrar ação no log
    INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                            vida_restante_jogador, vida_restante_inimigo, descricao_acao)
    VALUES (combate_id, proximo_turno_inimigo, 'inimigo', acao_inimigo, dano_causado,
            vida_jogador, vida_inimigo, resultado_acao);

    -- Verificar se jogador foi derrotado
    IF vida_jogador <= 0 THEN
        PERFORM finalizar_combate(combate_id, 'inimigo');
        resultado_acao := resultado_acao || ' Você foi derrotado!';
    END IF;

    RETURN resultado_acao;
END;
$$ LANGUAGE plpgsql;

-- Função para finalizar combate e distribuir recompensas
CREATE OR REPLACE FUNCTION finalizar_combate(combate_id INT, vencedor VARCHAR(10))
RETURNS TEXT AS $$
DECLARE
    jogador_id INT;
    inimigo_id INT;
    vida_final_jogador INT;
    xp_recompensa INT := 0;
    gcs_recompensa INT := 0;
    nivel_inimigo INT;
    creditos_inimigo INT;
    data_inicio_combate TIMESTAMP;
    duracao INTERVAL;
    total_turnos INT;
    dano_total_jogador INT;
    dano_total_inimigo INT;
    resultado_texto TEXT;
    jogador_level_atual INT;
    jogador_xp_atual INT;
    novo_level INT;
BEGIN
    -- Obter dados do combate
    SELECT id_player, id_mob, vida_jogador_atual, data_inicio
    INTO jogador_id, inimigo_id, vida_final_jogador, data_inicio_combate
    FROM Combate WHERE id_combate = combate_id;

    IF NOT FOUND THEN
        RETURN 'Erro: Combate não encontrado';
    END IF;

    -- Calcular duração
    duracao := CURRENT_TIMESTAMP - data_inicio_combate;

    -- Obter estatísticas do combate
    SELECT COUNT(*),
           COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0),
           COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0)
    INTO total_turnos, dano_total_jogador, dano_total_inimigo
    FROM Combate_Log WHERE id_combate = combate_id;

    -- Calcular recompensas se jogador venceu
    IF vencedor = 'jogador' THEN
        SELECT nivel, creditos INTO nivel_inimigo, creditos_inimigo
        FROM Inimigo WHERE id_mob = inimigo_id;

        -- XP baseado no nível do inimigo
        xp_recompensa := nivel_inimigo * 50 + 25;

        -- GCS baseado nos créditos do inimigo
        gcs_recompensa := creditos_inimigo;

        -- Atualizar jogador com recompensas
        SELECT level, xp INTO jogador_level_atual, jogador_xp_atual
        FROM Personagem WHERE id_player = jogador_id;

        -- Calcular novo level
        novo_level := GREATEST(jogador_level_atual, (jogador_xp_atual + xp_recompensa) / 1000 + 1);

        UPDATE Personagem
        SET xp = xp + xp_recompensa,
            gcs = gcs + gcs_recompensa,
            level = novo_level,
            vida_base = vida_final_jogador  -- Atualizar vida atual
        WHERE id_player = jogador_id;

        resultado_texto := 'Vitória! Você ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.';

        IF novo_level > jogador_level_atual THEN
            resultado_texto := resultado_texto || ' Level up! Novo level: ' || novo_level;
        END IF;

    ELSIF vencedor = 'inimigo' THEN
        -- Penalidades por morte
        DECLARE
            gcs_atual INT;
            vida_ressurreicao INT;
        BEGIN
            -- Obter GCS atual do jogador
            SELECT gcs INTO gcs_atual FROM Personagem WHERE id_player = jogador_id;

            -- Determinar vida de ressurreição baseada nos GCS
            IF gcs_atual >= 100 THEN
                vida_ressurreicao := 100;  -- Vida completa se tiver dinheiro
            ELSE
                vida_ressurreicao := 50;   -- Vida reduzida se não tiver dinheiro
            END IF;

            -- Aplicar penalidades
            UPDATE Personagem
            SET mortes = mortes + 1,
                gcs = GREATEST(gcs - 100, 0),  -- Perde 100 GCS (mínimo 0)
                xp = GREATEST(xp - (level * 10), 0),  -- Perde XP baseado no level
                vida_base = vida_ressurreicao  -- Vida baseada nos GCS disponíveis
            WHERE id_player = jogador_id;

            -- Mensagem personalizada baseada na situação
            IF gcs_atual >= 100 THEN
                resultado_texto := 'Derrota! Você foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.';
            ELSE
                resultado_texto := 'Derrota! Você foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).';
            END IF;
        END;
    ELSE
        -- Caso de fuga - manter vida atual
        UPDATE Personagem
        SET vida_base = vida_final_jogador
        WHERE id_player = jogador_id;

        resultado_texto := 'Você fugiu do combate.';
    END IF;

    -- Atualizar status do combate
    UPDATE Combate
    SET status_combate = 'finalizado', data_fim = CURRENT_TIMESTAMP
    WHERE id_combate = combate_id;

    -- Registrar resultado
    INSERT INTO Combate_Resultado (id_combate, vencedor, xp_ganho, gcs_ganho,
                                  duracao_combate, total_turnos, dano_total_jogador, dano_total_inimigo)
    VALUES (combate_id, vencedor, xp_recompensa, gcs_recompensa,
            duracao, total_turnos, dano_total_jogador, dano_total_inimigo);

    RETURN resultado_texto;
END;
$$ LANGUAGE plpgsql;

-- Função para obter status do combate atual do jogador
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
        c.turno_atual,
        COALESCE(MAX(cl.turno_numero), 0) as turno_numero
    FROM Combate c
    JOIN Inimigo i ON c.id_mob = i.id_mob
    LEFT JOIN Combate_Log cl ON c.id_combate = cl.id_combate
    WHERE c.id_player = jogador_id AND c.status_combate = 'ativo'
    GROUP BY c.id_combate, i.tipo_mob, c.vida_jogador_atual, c.vida_inimigo_atual, c.turno_atual;
END;
$$ LANGUAGE plpgsql;
