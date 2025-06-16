SELECT
    m.id_missao,
    m.valor_recompensa,
    m.status,
    m.nome_planeta,
    m.id_NPC,
    m.level_minimo,
    CASE
        WHEN md.id_missao IS NOT NULL THEN 'Missão Disponível'
        WHEN mc.id_missao IS NOT NULL THEN 'Missão Concluída'
        WHEN ma.id_missao IS NOT NULL THEN 'Missão em Andamento'
        ELSE 'Outro Status'
    END AS tipo_missao
FROM Missao m
LEFT JOIN Missao_Disponivel md ON m.id_missao = md.id_missao
LEFT JOIN Missao_Concluida mc ON m.id_missao = mc.id_missao
LEFT JOIN Missao_Em_Andamento ma ON m.id_missao = ma.id_missao;
