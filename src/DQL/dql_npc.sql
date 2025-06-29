-- ========================================
-- CONSULTAS DQL - NPCs
-- ========================================

-- 1. Lista todos os NPCs com suas especializações
SELECT
    n.id_NPC,
    n.nome_planeta,
    COALESCE(m.Itens_Disponiveis, 'N/A') AS itens_disponiveis,
    COALESCE(me.Servicos_disponiveis, 'N/A') AS servicos_disponiveis,
    CASE
        WHEN m.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN me.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'NPC Genérico'
    END AS tipo_npc
FROM Npc n
LEFT JOIN Mercante m ON n.id_NPC = m.id_NPC
LEFT JOIN Mecanico me ON n.id_NPC = me.id_NPC
ORDER BY n.nome_planeta, n.id_NPC;

-- 2. Lista apenas os Mercantes
SELECT
    n.id_NPC,
    n.nome_planeta,
    m.Itens_Disponiveis
FROM Npc n
INNER JOIN Mercante m ON n.id_NPC = m.id_NPC
ORDER BY n.nome_planeta;

-- 3. Lista apenas os Mecânicos
SELECT
    n.id_NPC,
    n.nome_planeta,
    me.Servicos_disponiveis
FROM Npc n
INNER JOIN Mecanico me ON n.id_NPC = me.id_NPC
ORDER BY n.nome_planeta;

-- 4. Conta NPCs por planeta
SELECT
    nome_planeta,
    COUNT(*) AS total_npcs,
    COUNT(m.id_NPC) AS total_mercantes,
    COUNT(me.id_NPC) AS total_mecanicos
FROM Npc n
LEFT JOIN Mercante m ON n.id_NPC = m.id_NPC
LEFT JOIN Mecanico me ON n.id_NPC = me.id_NPC
GROUP BY nome_planeta
ORDER BY total_npcs DESC;

-- 5. NPCs por tipo de especialização
SELECT
    CASE
        WHEN m.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN me.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'NPC Genérico'
    END AS tipo_npc,
    COUNT(*) AS quantidade
FROM Npc n
LEFT JOIN Mercante m ON n.id_NPC = m.id_NPC
LEFT JOIN Mecanico me ON n.id_NPC = me.id_NPC
GROUP BY
    CASE
        WHEN m.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN me.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'NPC Genérico'
    END
ORDER BY quantidade DESC;
