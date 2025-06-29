-- ========================================
-- CONSULTAS DQL - SISTEMAS ESTELARES
-- ========================================

-- 1. Lista todos os sistemas com informações dos planetas
SELECT
    s.id_sistema,
    s.nome_sistema,
    COUNT(p.nome_planeta) AS total_planetas,
    COUNT(CASE WHEN p.habitavel = true THEN 1 END) AS planetas_habitaveis,
    STRING_AGG(p.nome_planeta, ', ' ORDER BY p.nome_planeta) AS lista_planetas
FROM Sistema s
LEFT JOIN Planeta p ON s.id_sistema = p.id_sistema
GROUP BY s.id_sistema, s.nome_sistema
ORDER BY total_planetas DESC, s.nome_sistema;

-- 2. Sistemas com planetas habitáveis
SELECT
    s.id_sistema,
    s.nome_sistema,
    COUNT(p.nome_planeta) AS planetas_habitaveis,
    STRING_AGG(p.nome_planeta, ', ' ORDER BY p.nome_planeta) AS planetas
FROM Sistema s
INNER JOIN Planeta p ON s.id_sistema = p.id_sistema
WHERE p.habitavel = true
GROUP BY s.id_sistema, s.nome_sistema
ORDER BY planetas_habitaveis DESC;

-- 3. Classificação dos sistemas por tipo de clima predominante
SELECT
    s.id_sistema,
    s.nome_sistema,
    COUNT(p.nome_planeta) AS total_planetas,
    CASE
        WHEN COUNT(CASE WHEN LOWER(p.clima) LIKE '%desértico%' THEN 1 END) >
             COUNT(CASE WHEN LOWER(p.clima) NOT LIKE '%desértico%' THEN 1 END)
        THEN 'Sistema Desértico'
        WHEN COUNT(CASE WHEN LOWER(p.clima) LIKE '%temperado%' THEN 1 END) >
             COUNT(CASE WHEN LOWER(p.clima) NOT LIKE '%temperado%' THEN 1 END)
        THEN 'Sistema Temperado'
        WHEN COUNT(CASE WHEN LOWER(p.clima) LIKE '%tropical%' THEN 1 END) >
             COUNT(CASE WHEN LOWER(p.clima) NOT LIKE '%tropical%' THEN 1 END)
        THEN 'Sistema Tropical'
        WHEN COUNT(CASE WHEN LOWER(p.clima) LIKE '%gelado%' THEN 1 END) >
             COUNT(CASE WHEN LOWER(p.clima) NOT LIKE '%gelado%' THEN 1 END)
        THEN 'Sistema Gelado'
        ELSE 'Sistema Misto'
    END AS tipo_sistema_predominante
FROM Sistema s
LEFT JOIN Planeta p ON s.id_sistema = p.id_sistema
GROUP BY s.id_sistema, s.nome_sistema
ORDER BY total_planetas DESC;

-- 4. Sistemas sem planetas
SELECT
    s.id_sistema,
    s.nome_sistema
FROM Sistema s
LEFT JOIN Planeta p ON s.id_sistema = p.id_sistema
WHERE p.nome_planeta IS NULL
ORDER BY s.nome_sistema;

-- 5. Estatísticas gerais dos sistemas
SELECT
    COUNT(DISTINCT s.id_sistema) AS total_sistemas,
    COUNT(DISTINCT p.nome_planeta) AS total_planetas,
    AVG(planetas_por_sistema.total) AS media_planetas_por_sistema,
    MAX(planetas_por_sistema.total) AS max_planetas_sistema,
    MIN(planetas_por_sistema.total) AS min_planetas_sistema
FROM Sistema s
LEFT JOIN Planeta p ON s.id_sistema = p.id_sistema
CROSS JOIN (
    SELECT COUNT(p2.nome_planeta) AS total
    FROM Sistema s2
    LEFT JOIN Planeta p2 ON s2.id_sistema = p2.id_sistema
    GROUP BY s2.id_sistema
) AS planetas_por_sistema;
