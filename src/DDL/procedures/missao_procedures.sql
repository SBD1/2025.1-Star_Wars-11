-- PROCEDURES - SISTEMA DE MISSÕES

-- Aceitar missão (versão simplificada)
CREATE OR REPLACE FUNCTION aceitar_missao(
    p_id_player INT,
    p_id_missao INT
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    level_jogador INT;
    level_minimo INT;
    status_missao VARCHAR(20);
BEGIN
    SELECT p.level, m.level_minimo, m.status
    INTO level_jogador, level_minimo, status_missao
    FROM Personagem p, Missao m
    WHERE p.id_player = p_id_player AND m.id_missao = p_id_missao;
    
    IF level_jogador IS NULL THEN
        RAISE EXCEPTION 'Jogador ou missão não encontrados';
    END IF;
    
    IF status_missao != 'Disponível' THEN
        RAISE EXCEPTION 'Missão não está disponível';
    END IF;
    
    IF level_jogador < level_minimo THEN
        RAISE EXCEPTION 'Level insuficiente. Necessário: %, Atual: %', level_minimo, level_jogador;
    END IF;
    
    IF EXISTS (SELECT 1 FROM Missao_Jogador WHERE id_player = p_id_player AND id_missao = p_id_missao) THEN
        RAISE EXCEPTION 'Missão já aceita';
    END IF;
    
    INSERT INTO Missao_Jogador (id_player, id_missao, status_jogador)
    VALUES (p_id_player, p_id_missao, 'Em Andamento');
    
    RETURN TRUE;
END;
$$;

-- Abandonar missão
CREATE OR REPLACE FUNCTION abandonar_missao(
    p_id_player INT,
    p_id_missao INT
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM Missao_Jogador 
        WHERE id_player = p_id_player AND id_missao = p_id_missao 
        AND status_jogador = 'Em Andamento'
    ) THEN
        RAISE EXCEPTION 'Missão não está em andamento';
    END IF;
    
    DELETE FROM Missao_Jogador 
    WHERE id_player = p_id_player AND id_missao = p_id_missao;
    
    RETURN TRUE;
END;
$$;

-- Listar missões do jogador
CREATE OR REPLACE FUNCTION minhas_missoes(p_id_player INT)
RETURNS TABLE (
    id_missao INT, nome_missao VARCHAR(100), status_jogador VARCHAR(20),
    valor_recompensa INT, xp_recompensa INT, data_aceita TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id_missao, m.nome_missao, mj.status_jogador,
        m.valor_recompensa, m.xp_recompensa, mj.data_aceita
    FROM Missao_Jogador mj
    JOIN Missao m ON mj.id_missao = m.id_missao
    WHERE mj.id_player = p_id_player
    ORDER BY mj.data_aceita DESC;
END;
$$;

-- Missões disponíveis para o jogador
CREATE OR REPLACE FUNCTION missoes_disponiveis(p_id_player INT)
RETURNS TABLE (
    id_missao INT, nome_missao VARCHAR(100), descricao TEXT,
    valor_recompensa INT, xp_recompensa INT, level_minimo INT,
    nome_planeta VARCHAR(20), tipo_missao VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
DECLARE
    level_jogador INT;
BEGIN
    SELECT level INTO level_jogador FROM Personagem WHERE id_player = p_id_player;
    
    RETURN QUERY
    SELECT 
        m.id_missao, m.nome_missao, m.descricao,
        m.valor_recompensa, m.xp_recompensa, m.level_minimo,
        m.nome_planeta, m.tipo_missao
    FROM Missao m
    WHERE m.status = 'Disponível'
    AND m.level_minimo <= level_jogador
    AND NOT EXISTS (
        SELECT 1 FROM Missao_Jogador mj 
        WHERE mj.id_player = p_id_player AND mj.id_missao = m.id_missao
    )
    ORDER BY m.level_minimo, m.valor_recompensa DESC;
END;
$$;

-- Progresso de missões
CREATE OR REPLACE FUNCTION progresso_missoes(p_id_player INT)
RETURNS TABLE (
    total_missoes BIGINT, em_andamento BIGINT, concluidas BIGINT,
    total_xp_ganho BIGINT, total_creditos_ganhos BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) AS total_missoes,
        COUNT(CASE WHEN mj.status_jogador = 'Em Andamento' THEN 1 END) AS em_andamento,
        COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS concluidas,
        COALESCE(SUM(CASE WHEN mj.status_jogador = 'Concluída' THEN m.xp_recompensa ELSE 0 END), 0) AS total_xp_ganho,
        COALESCE(SUM(CASE WHEN mj.status_jogador = 'Concluída' THEN m.valor_recompensa ELSE 0 END), 0) AS total_creditos_ganhos
    FROM Missao_Jogador mj
    JOIN Missao m ON mj.id_missao = m.id_missao
    WHERE mj.id_player = p_id_player;
END;
$$;

-- Missões por planeta
CREATE OR REPLACE FUNCTION missoes_planeta(p_nome_planeta VARCHAR(20))
RETURNS TABLE (
    id_missao INT, nome_missao VARCHAR(100), level_minimo INT,
    valor_recompensa INT, tipo_missao VARCHAR(20), status VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id_missao, m.nome_missao, m.level_minimo,
        m.valor_recompensa, m.tipo_missao, m.status
    FROM Missao m
    WHERE m.nome_planeta = p_nome_planeta
    ORDER BY m.level_minimo, m.valor_recompensa DESC;
END;
$$;
