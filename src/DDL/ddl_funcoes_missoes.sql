--será a funcao responsável por listar as missões para o player
CREATE OR REPLACE FUNCTION listar_missoes_disponiveis(jogador_id INT)
RETURNS TABLE (
    id_missao INT,
    nome_missao VARCHAR(100),
    descricao TEXT,
    valor_recompensa INT,
    xp_recompensa INT,
    nome_planeta VARCHAR(20),
    level_minimo INT,
    tipo_missao VARCHAR(20),
    requisitos_especiais TEXT,
    npc_nome TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        m.id_missao,
        m.nome_missao,
        m.descricao,
        m.valor_recompensa,
        m.xp_recompensa,
        m.nome_planeta,
        m.level_minimo,
        m.tipo_missao,
        COALESCE(md.requisitos_especiais, '')::TEXT as requisitos_especiais,
        CASE
            WHEN mer.id_NPC IS NOT NULL THEN 'Mercante'::TEXT
            WHEN mec.id_NPC IS NOT NULL THEN 'Mecânico'::TEXT
            ELSE 'NPC'::TEXT
        END as npc_nome
    FROM Missao m
    JOIN Missao_Disponivel md ON m.id_missao = md.id_missao
    LEFT JOIN Mercante mer ON m.id_NPC = mer.id_NPC
    LEFT JOIN Mecanico mec ON m.id_NPC = mec.id_NPC
    LEFT JOIN Personagem p ON p.id_player = jogador_id
    LEFT JOIN Missao_Jogador mj ON m.id_missao = mj.id_missao AND mj.id_player = jogador_id
    WHERE m.status = 'Disponível'
      AND p.level >= m.level_minimo
      AND mj.id_missao IS NULL  -- Jogador ainda não aceitou esta missão
    ORDER BY m.level_minimo, m.valor_recompensa;
END;
$$ LANGUAGE plpgsql;

-- Função para aceitar uma missão
CREATE OR REPLACE FUNCTION aceitar_missao(jogador_id INT, missao_id INT)
RETURNS TEXT AS $$
DECLARE
    jogador_level INT;
    missao_level_min INT;
    jogador_planeta VARCHAR(20);
    missao_planeta VARCHAR(20);
    missao_nome VARCHAR(100);
    ja_aceita BOOLEAN;
BEGIN
    -- Verificar se o jogador existe e obter informações
    SELECT level, nome_planeta INTO jogador_level, jogador_planeta
    FROM Personagem WHERE id_player = jogador_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Jogador não encontrado';
    END IF;
    
    -- Verificar se a missão existe e obter informações
    SELECT level_minimo, nome_planeta, nome_missao INTO missao_level_min, missao_planeta, missao_nome
    FROM Missao WHERE id_missao = missao_id AND status = 'Disponível';
    
    IF NOT FOUND THEN
        RETURN 'Erro: Missão não encontrada ou não disponível';
    END IF;
    
    -- Verificar se o jogador já aceitou esta missão
    SELECT EXISTS(SELECT 1 FROM Missao_Jogador WHERE id_player = jogador_id AND id_missao = missao_id) INTO ja_aceita;
    
    IF ja_aceita THEN
        RETURN 'Erro: Você já aceitou esta missão';
    END IF;
    
    -- Verificar level mínimo
    IF jogador_level < missao_level_min THEN
        RETURN 'Erro: Level insuficiente. Necessário: ' || missao_level_min || ', Atual: ' || jogador_level;
    END IF;
    
    -- Verificar se o jogador está no planeta correto
    IF jogador_planeta != missao_planeta THEN
        RETURN 'Erro: Você precisa estar em ' || missao_planeta || ' para aceitar esta missão';
    END IF;
    
    -- Aceitar a missão
    INSERT INTO Missao_Jogador (id_player, id_missao, status_jogador, progresso)
    VALUES (jogador_id, missao_id, 'Em Andamento', 'Missão aceita');
    
    -- Atualizar contador de jogadores ativos
    UPDATE Missao_Em_Andamento 
    SET jogadores_ativos = jogadores_ativos + 1 
    WHERE id_missao = missao_id;
    
    RETURN 'Sucesso: Missão "' || missao_nome || '" aceita com sucesso!';
END;
$$ LANGUAGE plpgsql;

-- Função para listar missões do jogador
CREATE OR REPLACE FUNCTION listar_missoes_jogador(jogador_id INT)
RETURNS TABLE (
    id_missao INT,
    nome_missao VARCHAR(100),
    status_jogador VARCHAR(20),
    progresso TEXT,
    data_aceita TIMESTAMP,
    tipo_missao VARCHAR(20),
    valor_recompensa INT,
    xp_recompensa INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id_missao,
        m.nome_missao,
        mj.status_jogador,
        mj.progresso,
        mj.data_aceita,
        m.tipo_missao,
        m.valor_recompensa,
        m.xp_recompensa
    FROM Missao_Jogador mj
    JOIN Missao m ON mj.id_missao = m.id_missao
    WHERE mj.id_player = jogador_id
    ORDER BY mj.data_aceita DESC;
END;
$$ LANGUAGE plpgsql;

-- Função para concluir uma missão
CREATE OR REPLACE FUNCTION concluir_missao(jogador_id INT, missao_id INT)
RETURNS TEXT AS $$
DECLARE
    missao_recompensa INT;
    missao_xp INT;
    missao_nome VARCHAR(100);
    jogador_gcs INT;
    jogador_xp INT;
    jogador_level INT;
    novo_level INT;
    status_atual VARCHAR(20);
BEGIN
    -- Verificar se o jogador tem esta missão em andamento
    SELECT mj.status_jogador, m.valor_recompensa, m.xp_recompensa, m.nome_missao
    INTO status_atual, missao_recompensa, missao_xp, missao_nome
    FROM Missao_Jogador mj
    JOIN Missao m ON mj.id_missao = m.id_missao
    WHERE mj.id_player = jogador_id AND mj.id_missao = missao_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Você não possui esta missão';
    END IF;
    
    IF status_atual != 'Em Andamento' THEN
        RETURN 'Erro: Esta missão não está em andamento';
    END IF;
    
    -- Obter dados atuais do jogador
    SELECT gcs, xp, level INTO jogador_gcs, jogador_xp, jogador_level
    FROM Personagem WHERE id_player = jogador_id;
    
    -- Calcular novo level baseado no XP
    novo_level := GREATEST(jogador_level, (jogador_xp + missao_xp) / 1000 + 1);
    
    -- Atualizar jogador com recompensas
    UPDATE Personagem 
    SET gcs = gcs + missao_recompensa,
        xp = xp + missao_xp,
        level = novo_level
    WHERE id_player = jogador_id;
    
    -- Marcar missão como concluída
    UPDATE Missao_Jogador 
    SET status_jogador = 'Concluída',
        data_concluida = CURRENT_TIMESTAMP,
        progresso = 'Missão concluída com sucesso!'
    WHERE id_player = jogador_id AND id_missao = missao_id;
    
    -- Atualizar contadores
    UPDATE Missao_Em_Andamento 
    SET jogadores_ativos = GREATEST(0, jogadores_ativos - 1)
    WHERE id_missao = missao_id;
    
    UPDATE Missao_Concluida 
    SET total_conclusoes = total_conclusoes + 1
    WHERE id_missao = missao_id;
    
    RETURN 'Sucesso: Missão "' || missao_nome || '" concluída! Recompensas: ' || 
           missao_recompensa || ' GCS, ' || missao_xp || ' XP' ||
           CASE WHEN novo_level > jogador_level THEN '. Level up! Novo level: ' || novo_level ELSE '' END;
END;
$$ LANGUAGE plpgsql;

-- Função para abandonar uma missão
CREATE OR REPLACE FUNCTION abandonar_missao(jogador_id INT, missao_id INT)
RETURNS TEXT AS $$
DECLARE
    missao_nome VARCHAR(100);
    status_atual VARCHAR(20);
BEGIN
    -- Verificar se o jogador tem esta missão
    SELECT mj.status_jogador, m.nome_missao
    INTO status_atual, missao_nome
    FROM Missao_Jogador mj
    JOIN Missao m ON mj.id_missao = m.id_missao
    WHERE mj.id_player = jogador_id AND mj.id_missao = missao_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Você não possui esta missão';
    END IF;
    
    IF status_atual != 'Em Andamento' THEN
        RETURN 'Erro: Esta missão não pode ser abandonada';
    END IF;
    
    -- Remover a missão do jogador
    DELETE FROM Missao_Jogador 
    WHERE id_player = jogador_id AND id_missao = missao_id;
    
    -- Atualizar contador
    UPDATE Missao_Em_Andamento 
    SET jogadores_ativos = GREATEST(0, jogadores_ativos - 1)
    WHERE id_missao = missao_id;
    
    RETURN 'Missão "' || missao_nome || '" abandonada';
END;
$$ LANGUAGE plpgsql;
