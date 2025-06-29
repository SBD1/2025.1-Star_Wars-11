-- ========================================
-- CONSULTAS DQL - PLANETAS E SISTEMAS
-- ========================================

-- 1. Lista todos os planetas com informações do sistema
SELECT
    p.nome_planeta,
    p.habitavel,
    p.clima,
    p.id_sistema,
    s.nome_sistema,
    CASE
        WHEN LOWER(p.clima) LIKE '%desértico%' OR LOWER(p.clima) LIKE '%desert%' THEN 'Planeta Desértico'
        WHEN LOWER(p.clima) LIKE '%temperado%' OR LOWER(p.clima) LIKE '%temperate%' THEN 'Planeta Temperado'
        WHEN LOWER(p.clima) LIKE '%tropical%' THEN 'Planeta Tropical'
        WHEN LOWER(p.clima) LIKE '%gelado%' OR LOWER(p.clima) LIKE '%frio%' OR LOWER(p.clima) LIKE '%ice%' THEN 'Planeta Gelado'
        ELSE 'Outro Tipo'
    END AS tipo_planeta_clima
FROM Planeta p
INNER JOIN Sistema s ON p.id_sistema = s.id_sistema
ORDER BY s.nome_sistema, p.nome_planeta;

-- 2. Planetas habitáveis
SELECT
    p.nome_planeta,
    p.clima,
    s.nome_sistema,
    CASE
        WHEN LOWER(p.clima) LIKE '%desértico%' OR LOWER(p.clima) LIKE '%desert%' THEN 'Planeta Desértico'
        WHEN LOWER(p.clima) LIKE '%temperado%' OR LOWER(p.clima) LIKE '%temperate%' THEN 'Planeta Temperado'
        WHEN LOWER(p.clima) LIKE '%tropical%' THEN 'Planeta Tropical'
        WHEN LOWER(p.clima) LIKE '%gelado%' OR LOWER(p.clima) LIKE '%frio%' OR LOWER(p.clima) LIKE '%ice%' THEN 'Planeta Gelado'
        ELSE 'Outro Tipo'
    END AS tipo_clima
FROM Planeta p
INNER JOIN Sistema s ON p.id_sistema = s.id_sistema
WHERE p.habitavel = true
ORDER BY p.nome_planeta;

-- 3. Planetas por sistema
SELECT
    s.nome_sistema,
    COUNT(p.nome_planeta) AS total_planetas,
    COUNT(CASE WHEN p.habitavel = true THEN 1 END) AS planetas_habitaveis,
    COUNT(CASE WHEN p.habitavel = false THEN 1 END) AS planetas_nao_habitaveis
FROM Sistema s
LEFT JOIN Planeta p ON s.id_sistema = p.id_sistema
GROUP BY s.id_sistema, s.nome_sistema
ORDER BY total_planetas DESC;

-- 4. Estatísticas por tipo de clima
SELECT
    CASE
        WHEN LOWER(p.clima) LIKE '%desértico%' OR LOWER(p.clima) LIKE '%desert%' THEN 'Desértico'
        WHEN LOWER(p.clima) LIKE '%temperado%' OR LOWER(p.clima) LIKE '%temperate%' THEN 'Temperado'
        WHEN LOWER(p.clima) LIKE '%tropical%' THEN 'Tropical'
        WHEN LOWER(p.clima) LIKE '%gelado%' OR LOWER(p.clima) LIKE '%frio%' OR LOWER(p.clima) LIKE '%ice%' THEN 'Gelado'
        ELSE 'Outro'
    END AS tipo_clima,
    COUNT(*) AS quantidade,
    COUNT(CASE WHEN habitavel = true THEN 1 END) AS habitaveis
FROM Planeta p
GROUP BY
    CASE
        WHEN LOWER(p.clima) LIKE '%desértico%' OR LOWER(p.clima) LIKE '%desert%' THEN 'Desértico'
        WHEN LOWER(p.clima) LIKE '%temperado%' OR LOWER(p.clima) LIKE '%temperate%' THEN 'Temperado'
        WHEN LOWER(p.clima) LIKE '%tropical%' THEN 'Tropical'
        WHEN LOWER(p.clima) LIKE '%gelado%' OR LOWER(p.clima) LIKE '%frio%' OR LOWER(p.clima) LIKE '%ice%' THEN 'Gelado'
        ELSE 'Outro'
    END
ORDER BY quantidade DESC;

-- 5. Planetas com personagens (se existirem dados)
SELECT
    p.nome_planeta,
    p.habitavel,
    p.clima,
    s.nome_sistema,
    COUNT(pe.id_player) AS total_personagens
FROM Planeta p
INNER JOIN Sistema s ON p.id_sistema = s.id_sistema
LEFT JOIN Personagem pe ON p.nome_planeta = pe.nome_planeta
GROUP BY p.nome_planeta, p.habitavel, p.clima, s.nome_sistema
ORDER BY total_personagens DESC, p.nome_planeta;
