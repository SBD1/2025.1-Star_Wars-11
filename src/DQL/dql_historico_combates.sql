-- ========================================
-- DQL - HISTÓRICO DE COMBATES
-- Consultas para ver histórico de lutas
-- ========================================

-- 🎯 COMANDO PRINCIPAL: HISTÓRICO COMPLETO DE COMBATES
-- Use este comando para ver todos os combates de todos os jogadores
SELECT
    p.id_player AS "ID Jogador",
    p.nome_classe AS "Classe",
    p.level AS "Level",
    p.mortes AS "Mortes",
    i.tipo_mob AS "Inimigo",
    i.nivel AS "Nível Inimigo",
    CASE
        WHEN cr.vencedor = 'jogador' THEN '🏆 VITÓRIA'
        WHEN cr.vencedor = 'inimigo' THEN '💀 DERROTA'
        ELSE '🏃 FUGA'
    END AS "Resultado",
    cr.xp_ganho AS "XP Ganho",
    cr.gcs_ganho AS "GCS Ganho",
    cr.total_turnos AS "Turnos",
    cr.duracao_combate AS "Duração",
    c.data_inicio AS "Data/Hora"
FROM combate c
JOIN personagem p ON c.id_player = p.id_player
JOIN inimigo i ON c.id_mob = i.id_mob
JOIN combate_resultado cr ON c.id_combate = cr.id_combate
ORDER BY c.data_inicio DESC;

-- 📊 RESUMO ESTATÍSTICO POR JOGADOR
-- Estatísticas consolidadas de cada jogador
SELECT
    p.id_player AS "ID",
    p.nome_classe AS "Classe",
    p.level AS "Level",
    p.mortes AS "Mortes",
    COUNT(*) AS "Total Combates",
    SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) AS "Vitórias",
    SUM(CASE WHEN cr.vencedor = 'inimigo' THEN 1 ELSE 0 END) AS "Derrotas",
    SUM(CASE WHEN cr.vencedor = 'fuga' THEN 1 ELSE 0 END) AS "Fugas",
    ROUND(
        (SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 1
    ) AS "Taxa Vitória %",
    SUM(cr.xp_ganho) AS "Total XP",
    SUM(cr.gcs_ganho) AS "Total GCS"
FROM combate c
JOIN personagem p ON c.id_player = p.id_player
JOIN combate_resultado cr ON c.id_combate = cr.id_combate
GROUP BY p.id_player, p.nome_classe, p.level, p.mortes
ORDER BY "Vitórias" DESC, "Total Combates" DESC;

-- 🏆 TOP INIMIGOS MAIS ENFRENTADOS
-- Quais inimigos são mais comuns nas lutas
SELECT
    i.tipo_mob AS "Tipo de Inimigo",
    i.nivel AS "Nível",
    COUNT(*) AS "Vezes Enfrentado",
    SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) AS "Derrotado pelo Jogador",
    SUM(CASE WHEN cr.vencedor = 'inimigo' THEN 1 ELSE 0 END) AS "Derrotou o Jogador",
    ROUND(
        (SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 1
    ) AS "Taxa Derrota do Inimigo %"
FROM combate c
JOIN inimigo i ON c.id_mob = i.id_mob
JOIN combate_resultado cr ON c.id_combate = cr.id_combate
GROUP BY i.tipo_mob, i.nivel
ORDER BY "Vezes Enfrentado" DESC;

-- 🕐 COMBATES RECENTES (ÚLTIMAS 24 HORAS)
-- Atividade recente de combate
SELECT
    p.nome_classe AS "Jogador",
    i.tipo_mob AS "Inimigo",
    CASE
        WHEN cr.vencedor = 'jogador' THEN '🏆 VITÓRIA'
        WHEN cr.vencedor = 'inimigo' THEN '💀 DERROTA'
        ELSE '🏃 FUGA'
    END AS "Resultado",
    cr.total_turnos AS "Turnos",
    c.data_inicio AS "Quando"
FROM combate c
JOIN personagem p ON c.id_player = p.id_player
JOIN inimigo i ON c.id_mob = i.id_mob
JOIN combate_resultado cr ON c.id_combate = cr.id_combate
WHERE c.data_inicio >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY c.data_inicio DESC;

-- 🎮 COMBATES ATIVOS (SE HOUVER)
-- Mostra combates que estão acontecendo agora
SELECT
    c.id_combate AS "ID Combate",
    p.nome_classe AS "Jogador",
    i.tipo_mob AS "Inimigo",
    c.vida_jogador_atual AS "Vida Jogador",
    c.vida_inimigo_atual AS "Vida Inimigo",
    c.turno_atual AS "Turno",
    c.data_inicio AS "Iniciado em"
FROM combate c
JOIN personagem p ON c.id_player = p.id_player
JOIN inimigo i ON c.id_mob = i.id_mob
WHERE c.status_combate = 'ativo'
ORDER BY c.data_inicio DESC;

-- 💀 HISTÓRICO DE MORTES
-- Quando e como cada jogador morreu
SELECT
    p.nome_classe AS "Jogador",
    p.mortes AS "Total de Mortes",
    i.tipo_mob AS "Morto por",
    i.nivel AS "Nível do Inimigo",
    cr.total_turnos AS "Turnos até Morte",
    c.data_inicio AS "Data da Morte"
FROM combate c
JOIN personagem p ON c.id_player = p.id_player
JOIN inimigo i ON c.id_mob = i.id_mob
JOIN combate_resultado cr ON c.id_combate = cr.id_combate
WHERE cr.vencedor = 'inimigo'
ORDER BY c.data_inicio DESC;
