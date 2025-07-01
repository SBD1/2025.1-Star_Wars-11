-- PROCEDURES - SISTEMA DE COMBATE

-- Iniciar combate contra inimigo
CREATE OR REPLACE FUNCTION iniciar_combate(
    p_id_player INT,
    p_id_mob INT
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    poder_jogador INT;
    poder_inimigo INT;
    xp_ganho INT;
    creditos_ganhos INT;
    venceu BOOLEAN;
    resultado JSON;
BEGIN
    SELECT (vida_base + dano_base + level * 10) INTO poder_jogador
    FROM Personagem WHERE id_player = p_id_player;
    
    SELECT (vida_base + dano_base), creditos INTO poder_inimigo, creditos_ganhos
    FROM Inimigo WHERE id_mob = p_id_mob;
    
    IF poder_jogador IS NULL THEN
        RAISE EXCEPTION 'Jogador não encontrado';
    END IF;
    
    IF poder_inimigo IS NULL THEN
        RAISE EXCEPTION 'Inimigo não encontrado';
    END IF;
    
    venceu := poder_jogador > poder_inimigo;
    
    IF venceu THEN
        xp_ganho := poder_inimigo / 10;
        UPDATE Personagem 
        SET xp = xp + xp_ganho, gcs = gcs + creditos_ganhos
        WHERE id_player = p_id_player;
        
        -- Verificar se subiu de level
        PERFORM subir_level(p_id_player);
    ELSE
        xp_ganho := 0;
        creditos_ganhos := 0;
    END IF;
    
    resultado := json_build_object(
        'vencedor', CASE WHEN venceu THEN 'Jogador' ELSE 'Inimigo' END,
        'poder_jogador', poder_jogador,
        'poder_inimigo', poder_inimigo,
        'xp_ganho', xp_ganho,
        'creditos_ganhos', creditos_ganhos
    );
    
    RETURN resultado;
END;
$$;

-- Calcular dano de ataque
CREATE OR REPLACE FUNCTION calcular_dano(
    p_dano_base INT,
    p_level INT,
    p_tipo_ataque VARCHAR(20) DEFAULT 'normal'
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    dano_final INT;
    multiplicador DECIMAL;
BEGIN
    CASE p_tipo_ataque
        WHEN 'critico' THEN multiplicador := 2.0;
        WHEN 'especial' THEN multiplicador := 1.5;
        ELSE multiplicador := 1.0;
    END CASE;
    
    dano_final := (p_dano_base + (p_level * 2)) * multiplicador;
    
    RETURN dano_final;
END;
$$;

-- Verificar inimigos disponíveis por planeta
CREATE OR REPLACE FUNCTION inimigos_planeta(p_nome_planeta VARCHAR(20))
RETURNS TABLE (
    id_mob INT, tipo_mob VARCHAR(22), nivel INT, 
    vida_base INT, dano_base INT, creditos INT, nivel_ameaca INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id_mob, i.tipo_mob, i.nivel,
        i.vida_base, i.dano_base, i.creditos,
        m.nivel_ameaca
    FROM Inimigo i
    JOIN MOB m ON i.tipo_mob = m.tipo_mob
    WHERE i.planeta_origem = p_nome_planeta
    ORDER BY i.nivel, m.nivel_ameaca;
END;
$$;

-- Simular combate completo (versão avançada)
CREATE OR REPLACE FUNCTION simular_combate(
    p_id_player INT,
    p_id_mob INT
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    vida_jogador INT; dano_jogador INT; level_jogador INT;
    vida_inimigo INT; dano_inimigo INT; nivel_inimigo INT;
    vida_atual_jogador INT; vida_atual_inimigo INT;
    turno INT := 1;
    vencedor VARCHAR(20);
    log_combate TEXT := '';
    resultado JSON;
BEGIN
    -- Obter stats
    SELECT vida_base, dano_base, level 
    INTO vida_jogador, dano_jogador, level_jogador
    FROM Personagem WHERE id_player = p_id_player;
    
    SELECT vida_base, dano_base, nivel
    INTO vida_inimigo, dano_inimigo, nivel_inimigo
    FROM Inimigo WHERE id_mob = p_id_mob;
    
    vida_atual_jogador := vida_jogador;
    vida_atual_inimigo := vida_inimigo;
    
    -- Simular turnos
    WHILE vida_atual_jogador > 0 AND vida_atual_inimigo > 0 AND turno <= 10 LOOP
        -- Turno do jogador
        vida_atual_inimigo := vida_atual_inimigo - calcular_dano(dano_jogador, level_jogador);
        log_combate := log_combate || format('Turno %s: Jogador ataca (%s dano). ', turno, calcular_dano(dano_jogador, level_jogador));
        
        IF vida_atual_inimigo <= 0 THEN
            vencedor := 'Jogador';
            EXIT;
        END IF;
        
        -- Turno do inimigo
        vida_atual_jogador := vida_atual_jogador - calcular_dano(dano_inimigo, nivel_inimigo);
        log_combate := log_combate || format('Inimigo ataca (%s dano). ', calcular_dano(dano_inimigo, nivel_inimigo));
        
        IF vida_atual_jogador <= 0 THEN
            vencedor := 'Inimigo';
            EXIT;
        END IF;
        
        turno := turno + 1;
    END LOOP;
    
    -- Se chegou ao limite de turnos
    IF turno > 10 THEN
        vencedor := 'Empate';
    END IF;
    
    resultado := json_build_object(
        'vencedor', vencedor,
        'turnos', turno - 1,
        'vida_final_jogador', GREATEST(0, vida_atual_jogador),
        'vida_final_inimigo', GREATEST(0, vida_atual_inimigo),
        'log_combate', log_combate
    );
    
    RETURN resultado;
END;
$$;
