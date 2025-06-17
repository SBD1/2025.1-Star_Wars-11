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
        WHEN md.id_missao IS NOT NULL THEN 'Missão Disponível'
        WHEN mc.id_missao IS NOT NULL THEN 'Missão Concluída'
        WHEN ma.id_missao IS NOT NULL THEN 'Missão em Andamento'
        ELSE 'Outro Status'
    END AS categoria_missao,
    COALESCE(md.requisitos_especiais, '') as requisitos_especiais,
    COALESCE(ma.jogadores_ativos, 0) as jogadores_ativos,
    COALESCE(mc.total_conclusoes, 0) as total_conclusoes,
    CASE
        WHEN mer.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN mec.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'NPC Genérico'
    END AS tipo_npc
FROM Missao m
LEFT JOIN Missao_Disponivel md ON m.id_missao = md.id_missao
LEFT JOIN Missao_Concluida mc ON m.id_missao = mc.id_missao
LEFT JOIN Missao_Em_Andamento ma ON m.id_missao = ma.id_missao
LEFT JOIN Mercante mer ON m.id_NPC = mer.id_NPC
LEFT JOIN Mecanico mec ON m.id_NPC = mec.id_NPC
ORDER BY m.level_minimo, m.valor_recompensa;

-- Consulta de missões por jogador específico
-- SELECT * FROM listar_missoes_jogador(1);

-- Consulta de missões disponíveis para um jogador específico
-- SELECT * FROM listar_missoes_disponiveis(1);

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
