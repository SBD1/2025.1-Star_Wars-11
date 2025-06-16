SELECT
    s.id_sistema,
    s.nome_sistema,
    CASE
        WHEN sd.id_sistema IS NOT NULL THEN 'Sistema Desértico'
        WHEN su.id_sistema IS NOT NULL THEN 'Sistema Urbano'
        WHEN sf.id_sistema IS NOT NULL THEN 'Sistema Florestal'
        WHEN st.id_sistema IS NOT NULL THEN 'Sistema Tropical'
        ELSE 'Outro Tipo'
    END AS tipo_sistema
FROM Sistema s
LEFT JOIN Sistema_Desertico sd ON s.id_sistema = sd.id_sistema
LEFT JOIN Sistema_Urbano su ON s.id_sistema = su.id_sistema
LEFT JOIN Sistema_Florestal sf ON s.id_sistema = sf.id_sistema
LEFT JOIN Sistema_Tropical st ON s.id_sistema = st.id_sistema;
