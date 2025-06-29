-- ========================================
-- CONSULTAS DQL - PERSONAGENS, CLASSES E PLANETAS
-- ========================================

-- 1. Lista todos os personagens com informações de classe
SELECT
    p.id_player,
    p.vida_base,
    p.level,
    p.dano_base,
    p.xp,
    p.gcs,
    p.nome_classe,
    p.nome_planeta,
    c.Determinacao
FROM Personagem p
LEFT JOIN Classe c ON p.nome_classe = c.nome_classe
ORDER BY p.level DESC, p.xp DESC;

-- 2. Personagens Jedi com suas habilidades
SELECT
    p.id_player,
    p.level,
    p.vida_base,
    p.dano_base,
    p.nome_planeta,
    j.Force_Heal,
    j.Force_Vision,
    j.Defensive_Force_Shield
FROM Personagem p
INNER JOIN Jedi j ON p.nome_classe = j.nome_classe
ORDER BY p.level DESC;

-- 3. Personagens Sith com suas habilidades
SELECT
    p.id_player,
    p.level,
    p.vida_base,
    p.dano_base,
    p.nome_planeta,
    s.Force_Corruption,
    s.Force_Lightning,
    s.Essence_Transfer
FROM Personagem p
INNER JOIN Sith s ON p.nome_classe = s.nome_classe
ORDER BY p.level DESC;

-- 4. Personagens Caçadores de Recompensa com suas habilidades
SELECT
    p.id_player,
    p.level,
    p.vida_base,
    p.dano_base,
    p.nome_planeta,
    cr.Arsenal,
    cr.Master_Tracker,
    cr.Clocking_Device
FROM Personagem p
INNER JOIN Cacador_de_Recompensas cr ON p.nome_classe = cr.nome_classe
ORDER BY p.level DESC;

-- 5. Estatísticas por classe
SELECT
    c.nome_classe,
    c.Determinacao,
    COUNT(p.id_player) AS total_personagens,
    AVG(p.level) AS level_medio,
    AVG(p.vida_base) AS vida_media,
    AVG(p.dano_base) AS dano_medio,
    MAX(p.level) AS level_maximo,
    SUM(p.gcs) AS total_gcs
FROM Classe c
LEFT JOIN Personagem p ON c.nome_classe = p.nome_classe
GROUP BY c.nome_classe, c.Determinacao
ORDER BY total_personagens DESC;

-- 6. Personagens por planeta
SELECT
    nome_planeta,
    COUNT(*) AS total_personagens,
    AVG(level) AS level_medio,
    COUNT(CASE WHEN nome_classe = 'Jedi' THEN 1 END) AS total_jedi,
    COUNT(CASE WHEN nome_classe = 'Sith' THEN 1 END) AS total_sith,
    COUNT(CASE WHEN nome_classe = 'Cacador_de_Recompensas' THEN 1 END) AS total_cacadores
FROM Personagem
GROUP BY nome_planeta
ORDER BY total_personagens DESC;

-- 7. Top 10 personagens por XP
SELECT
    p.id_player,
    p.level,
    p.xp,
    p.nome_classe,
    p.nome_planeta,
    c.Determinacao
FROM Personagem p
INNER JOIN Classe c ON p.nome_classe = c.nome_classe
ORDER BY p.xp DESC
LIMIT 10;