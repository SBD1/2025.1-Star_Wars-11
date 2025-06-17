SELECT 
    n.id_NPC,
    n.nome_planeta,
    m.Itens_Disponiveis,
    me.Servicos_disponiveis,
    CASE 
        WHEN m.id_NPC IS NOT NULL THEN 'Mercante'
        WHEN me.id_NPC IS NOT NULL THEN 'Mecânico'
        ELSE 'Outro NPC'
    END AS tipo_npc
FROM Npc n
LEFT JOIN Mercante m ON n.id_NPC = m.id_NPC
LEFT JOIN Mecanico me ON n.id_NPC = me.id_NPC
ORDER BY n.id_NPC;
