SELECT
    p.nome_planeta,
    p.habitavel,
    p.clima,
    p.id_sistema,
    CASE
        WHEN pd.nome_planeta IS NOT NULL THEN 'Planeta Desértico'
        WHEN pt.nome_planeta IS NOT NULL THEN 'Planeta Temperado'
        WHEN ptr.nome_planeta IS NOT NULL THEN 'Planeta Tropical'
        WHEN pg.nome_planeta IS NOT NULL THEN 'Planeta Gelado'
        ELSE 'Outro Tipo'
    END AS tipo_planeta
FROM Planeta p
LEFT JOIN Planeta_Desertico pd ON p.nome_planeta = pd.nome_planeta
LEFT JOIN Planeta_Temperado pt ON p.nome_planeta = pt.nome_planeta
LEFT JOIN Planeta_Tropical ptr ON p.nome_planeta = ptr.nome_planeta
LEFT JOIN Planeta_Gelado pg ON p.nome_planeta = pg.nome_planeta;
