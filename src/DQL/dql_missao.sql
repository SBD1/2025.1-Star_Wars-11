-- ========================================
-- CONSULTAS DQL - MISSÕES
-- ========================================

-- 1. Lista todas as missões com informações do NPC
SELECT
    m.id_missao,
    m.nome_missao,
    m.descricao,
    m.valor_recompensa,
    m.xp_recompensa,
    m.status,
    m.nome_planeta,
    m.id_NPC,
    m.level_minimo,
    m.tipo_missao,
    CASE
        WHEN mer.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN mec.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'NPC Genérico'
    END AS tipo_npc,
    COALESCE(mer.Itens_Disponiveis, mec.Servicos_disponiveis, 'N/A') AS especialidade_npc
FROM Missao m
LEFT JOIN Mercante mer ON m.id_NPC = mer.id_NPC
LEFT JOIN Mecanico mec ON m.id_NPC = mec.id_NPC
ORDER BY m.level_minimo, m.valor_recompensa DESC;

-- 2. Missões disponíveis por nível mínimo
SELECT
    m.level_minimo,
    COUNT(*) AS total_missoes,
    AVG(m.valor_recompensa) AS recompensa_media,
    AVG(m.xp_recompensa) AS xp_medio,
    STRING_AGG(m.nome_missao, ', ' ORDER BY m.valor_recompensa DESC) AS lista_missoes
FROM Missao m
WHERE m.status = 'Disponível'
GROUP BY m.level_minimo
ORDER BY m.level_minimo;

-- 3. Missões por planeta
SELECT
    m.nome_planeta,
    COUNT(*) AS total_missoes,
    AVG(m.valor_recompensa) AS recompensa_media,
    AVG(m.level_minimo) AS level_minimo_medio,
    COUNT(CASE WHEN m.status = 'Disponível' THEN 1 END) AS missoes_disponiveis
FROM Missao m
GROUP BY m.nome_planeta
ORDER BY total_missoes DESC;

-- 4. Missões por tipo
SELECT
    m.tipo_missao,
    COUNT(*) AS quantidade,
    AVG(m.valor_recompensa) AS recompensa_media,
    AVG(m.xp_recompensa) AS xp_medio,
    MIN(m.level_minimo) AS level_minimo,
    MAX(m.level_minimo) AS level_maximo
FROM Missao m
GROUP BY m.tipo_missao
ORDER BY quantidade DESC;

-- 5. Missões com maior recompensa
SELECT
    m.id_missao,
    m.nome_missao,
    m.valor_recompensa,
    m.xp_recompensa,
    m.level_minimo,
    m.nome_planeta,
    m.tipo_missao
FROM Missao m
WHERE m.valor_recompensa > (SELECT AVG(valor_recompensa) FROM Missao)
ORDER BY m.valor_recompensa DESC;

-- 6. Estatísticas de missões por jogador (se houver dados)
SELECT
    mj.id_player,
    COUNT(*) AS total_missoes_aceitas,
    COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS missoes_concluidas,
    COUNT(CASE WHEN mj.status_jogador = 'Em Andamento' THEN 1 END) AS missoes_em_andamento,
    SUM(CASE WHEN mj.status_jogador = 'Concluída' THEN m.valor_recompensa ELSE 0 END) AS total_recompensas,
    SUM(CASE WHEN mj.status_jogador = 'Concluída' THEN m.xp_recompensa ELSE 0 END) AS total_xp_ganho
FROM Missao_Jogador mj
INNER JOIN Missao m ON mj.id_missao = m.id_missao
GROUP BY mj.id_player
ORDER BY total_recompensas DESC;

-- 7. Missões mais populares (mais aceitas pelos jogadores)
SELECT
    m.id_missao,
    m.nome_missao,
    m.valor_recompensa,
    m.level_minimo,
    COUNT(mj.id_player) AS vezes_aceita,
    COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS vezes_concluida
FROM Missao m
LEFT JOIN Missao_Jogador mj ON m.id_missao = mj.id_missao
GROUP BY m.id_missao, m.nome_missao, m.valor_recompensa, m.level_minimo
ORDER BY vezes_aceita DESC, vezes_concluida DESC;

-- Estatísticas de missões por planeta
SELECT
    nome_planeta,
    COUNT(*) as total_missoes,
    COUNT(CASE WHEN status = 'Disponível' THEN 1 END) as disponiveis,
    AVG(valor_recompensa) as recompensa_media,
    AVG(level_minimo) as level_medio_necessario
FROM Missao
GROUP BY nome_planeta
ORDER BY total_missoes DESC;
