-- ========================================
-- CONSULTAS DQL AVANÇADAS - STAR WARS MUD
-- ========================================

-- 1. Dashboard completo de um jogador
SELECT 
    p.id_player,
    p.level,
    p.vida_base,
    p.dano_base,
    p.xp,
    p.gcs,
    p.nome_classe,
    p.nome_planeta,
    c.Determinacao,
    COUNT(DISTINCT n.modelo) AS total_naves,
    COUNT(DISTINCT mj.id_missao) AS missoes_aceitas,
    COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS missoes_concluidas,
    COALESCE(inv_stats.total_itens, 0) AS total_itens_inventario,
    COALESCE(inv_stats.valor_inventario, 0) AS valor_total_inventario
FROM Personagem p
LEFT JOIN Classe c ON p.nome_classe = c.nome_classe
LEFT JOIN Nave n ON p.id_player = n.Id_Player
LEFT JOIN Missao_Jogador mj ON p.id_player = mj.id_player
LEFT JOIN (
    SELECT 
        inv.Id_Player,
        SUM(ii.quantidade) AS total_itens,
        SUM(i.preco * ii.quantidade) AS valor_inventario
    FROM Inventario inv
    LEFT JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
    LEFT JOIN Item i ON ii.id_item = i.id_item
    GROUP BY inv.Id_Player
) inv_stats ON p.id_player = inv_stats.Id_Player
WHERE p.id_player = 1  -- troca o id que deve ser visto
GROUP BY p.id_player, p.level, p.vida_base, p.dano_base, p.xp, p.gcs, 
         p.nome_classe, p.nome_planeta, c.Determinacao, 
         inv_stats.total_itens, inv_stats.valor_inventario;

-- 2. Ranking de jogadores por poder de combate
SELECT 
    p.id_player,
    p.level,
    p.vida_base,
    p.dano_base,
    p.xp,
    p.nome_classe,
    p.nome_planeta,
    (p.level * 10 + p.vida_base + p.dano_base + (p.xp / 100)) AS poder_combate,
    RANK() OVER (ORDER BY (p.level * 10 + p.vida_base + p.dano_base + (p.xp / 100)) DESC) AS ranking
FROM Personagem p
ORDER BY poder_combate DESC;

-- 3. Análise de economia do jogo
SELECT 
    'Personagens' AS categoria,
    SUM(p.gcs) AS total_creditos,
    AVG(p.gcs) AS media_creditos,
    COUNT(*) AS quantidade
FROM Personagem p
UNION ALL
SELECT 
    'Inventários' AS categoria,
    SUM(i.preco * ii.quantidade) AS total_creditos,
    AVG(i.preco * ii.quantidade) AS media_creditos,
    COUNT(DISTINCT ii.Id_PlayerIn) AS quantidade
FROM Inventario_Item ii
INNER JOIN Item i ON ii.id_item = i.id_item
UNION ALL
SELECT 
    'Missões Disponíveis' AS categoria,
    SUM(m.valor_recompensa) AS total_creditos,
    AVG(m.valor_recompensa) AS media_creditos,
    COUNT(*) AS quantidade
FROM Missao m
WHERE m.status = 'Disponível';

-- 4. Mapa de atividade por planeta
SELECT 
    pl.nome_planeta,
    pl.habitavel,
    pl.clima,
    s.nome_sistema,
    COUNT(DISTINCT p.id_player) AS personagens_presentes,
    COUNT(DISTINCT n.id_NPC) AS npcs_presentes,
    COUNT(DISTINCT m.id_missao) AS missoes_disponiveis,
    COUNT(DISTINCT i.id_mob) AS inimigos_nativos,
    CASE 
        WHEN COUNT(DISTINCT p.id_player) > 0 THEN 'Ativo'
        WHEN COUNT(DISTINCT m.id_missao) > 0 THEN 'Com Missões'
        WHEN COUNT(DISTINCT n.id_NPC) > 0 THEN 'Com NPCs'
        ELSE 'Inativo'
    END AS status_atividade
FROM Planeta pl
INNER JOIN Sistema s ON pl.id_sistema = s.id_sistema
LEFT JOIN Personagem p ON pl.nome_planeta = p.nome_planeta
LEFT JOIN Npc n ON pl.nome_planeta = n.nome_planeta
LEFT JOIN Missao m ON pl.nome_planeta = m.nome_planeta
LEFT JOIN Inimigo i ON pl.nome_planeta = i.planeta_origem
GROUP BY pl.nome_planeta, pl.habitavel, pl.clima, s.nome_sistema
ORDER BY personagens_presentes DESC, missoes_disponiveis DESC;

-- 5. Análise de balanceamento de classes
SELECT 
    c.nome_classe,
    c.Determinacao,
    COUNT(p.id_player) AS total_jogadores,
    AVG(p.level) AS level_medio,
    AVG(p.vida_base) AS vida_media,
    AVG(p.dano_base) AS dano_medio,
    AVG(p.xp) AS xp_medio,
    AVG(p.gcs) AS creditos_medio,
    COUNT(DISTINCT n.modelo) AS total_naves,
    AVG(missoes_stats.missoes_concluidas) AS media_missoes_concluidas
FROM Classe c
LEFT JOIN Personagem p ON c.nome_classe = p.nome_classe
LEFT JOIN Nave n ON p.id_player = n.Id_Player
LEFT JOIN (
    SELECT 
        p2.id_player,
        COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS missoes_concluidas
    FROM Personagem p2
    LEFT JOIN Missao_Jogador mj ON p2.id_player = mj.id_player
    GROUP BY p2.id_player
) missoes_stats ON p.id_player = missoes_stats.id_player
GROUP BY c.nome_classe, c.Determinacao
ORDER BY total_jogadores DESC;

-- 6. Relatório de segurança por planeta (baseado em inimigos)
SELECT 
    pl.nome_planeta,
    COUNT(i.id_mob) AS total_inimigos,
    AVG(i.nivel) AS nivel_ameaca_medio,
    AVG(i.vida_base) AS vida_media_inimigos,
    AVG(i.dano_base) AS dano_medio_inimigos,
    COUNT(CASE WHEN i.nivel >= 5 THEN 1 END) AS inimigos_perigosos,
    CASE 
        WHEN AVG(i.nivel) >= 7 THEN 'Muito Perigoso'
        WHEN AVG(i.nivel) >= 5 THEN 'Perigoso'
        WHEN AVG(i.nivel) >= 3 THEN 'Moderado'
        WHEN AVG(i.nivel) >= 1 THEN 'Seguro'
        ELSE 'Muito Seguro'
    END AS classificacao_seguranca
FROM Planeta pl
LEFT JOIN Inimigo i ON pl.nome_planeta = i.planeta_origem
GROUP BY pl.nome_planeta
ORDER BY nivel_ameaca_medio DESC NULLS LAST;

-- 7. Análise de progressão de XP necessário por level
WITH level_analysis AS (
    SELECT 
        level,
        COUNT(*) AS jogadores_neste_level,
        AVG(xp) AS xp_medio_level,
        MIN(xp) AS xp_minimo_level,
        MAX(xp) AS xp_maximo_level
    FROM Personagem
    GROUP BY level
)
SELECT 
    la.level,
    la.jogadores_neste_level,
    la.xp_medio_level,
    la.xp_minimo_level,
    la.xp_maximo_level,
    COALESCE(la_next.xp_minimo_level - la.xp_maximo_level, 0) AS xp_gap_proximo_level
FROM level_analysis la
LEFT JOIN level_analysis la_next ON la.level + 1 = la_next.level
ORDER BY la.level;
