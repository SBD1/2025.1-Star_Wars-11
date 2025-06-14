SELECT 
    n.modelo,
    n.velocidade,
    n.capacidade,
    CASE 
        WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
        WHEN y.modelo IS NOT NULL THEN 'YT-1300'
        WHEN l.modelo IS NOT NULL THEN 'Lambda Shuttle'
        WHEN f.modelo IS NOT NULL THEN 'Fregata CR90'
    END as tipo_nave
FROM Nave n
LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
LEFT JOIN YT_1300 y ON n.modelo = y.modelo
LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo;