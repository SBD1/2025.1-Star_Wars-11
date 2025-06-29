-- ========================================
-- CONSULTAS DQL - NAVES
-- ========================================

-- 1. Lista todas as naves com seus tipos e proprietários
SELECT
    n.modelo,
    n.Id_Player,
    n.velocidade,
    n.capacidade,
    CASE
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Class Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata Corelliana CR90'
        ELSE 'Tipo Desconhecido'
    END AS tipo_nave
FROM Nave n
LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
LEFT JOIN YT_1300 y ON n.modelo = y.modelo
LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo
ORDER BY n.velocidade DESC;

-- 2. Naves por tipo
SELECT
    CASE
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Class Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata Corelliana CR90'
        ELSE 'Tipo Desconhecido'
    END AS tipo_nave,
    COUNT(*) AS quantidade,
    AVG(n.velocidade) AS velocidade_media,
    AVG(n.capacidade) AS capacidade_media
FROM Nave n
LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
LEFT JOIN YT_1300 y ON n.modelo = y.modelo
LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo
GROUP BY
    CASE
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Class Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata Corelliana CR90'
        ELSE 'Tipo Desconhecido'
    END
ORDER BY quantidade DESC;

-- 3. Naves sem proprietário
SELECT
    n.modelo,
    n.velocidade,
    n.capacidade,
    CASE
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Class Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata Corelliana CR90'
        ELSE 'Tipo Desconhecido'
    END AS tipo_nave
FROM Nave n
LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
LEFT JOIN YT_1300 y ON n.modelo = y.modelo
LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo
WHERE n.Id_Player IS NULL
ORDER BY n.velocidade DESC;

-- 4. Naves mais rápidas
SELECT
    n.modelo,
    n.Id_Player,
    n.velocidade,
    n.capacidade,
    CASE
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Class Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata Corelliana CR90'
        ELSE 'Tipo Desconhecido'
    END AS tipo_nave
FROM Nave n
LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
LEFT JOIN YT_1300 y ON n.modelo = y.modelo
LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo
WHERE n.velocidade > (SELECT AVG(velocidade) FROM Nave)
ORDER BY n.velocidade DESC;

-- 5. Estatísticas gerais das naves
SELECT
    COUNT(*) AS total_naves,
    COUNT(Id_Player) AS naves_com_proprietario,
    COUNT(*) - COUNT(Id_Player) AS naves_sem_proprietario,
    AVG(velocidade) AS velocidade_media,
    MAX(velocidade) AS velocidade_maxima,
    MIN(velocidade) AS velocidade_minima,
    AVG(capacidade) AS capacidade_media,
    MAX(capacidade) AS capacidade_maxima,
    MIN(capacidade) AS capacidade_minima
FROM Nave;