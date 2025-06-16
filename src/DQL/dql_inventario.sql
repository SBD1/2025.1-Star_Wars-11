SELECT 
    ii.Id_PlayerIn,
    i.nome,
    i.peso,
    ii.quantidade,
    (i.peso * ii.quantidade) AS peso_total_item,
    CASE 
        WHEN i.tipo = 'arma' THEN 'Item de Ataque'
        WHEN i.tipo = 'armadura' THEN 'Item de Defesa'
        WHEN i.tipo = 'consumivel' THEN 'Item de Uso Temporário'
        WHEN i.tipo = 'especial' THEN 'Item Especial'
        ELSE 'Outro Tipo'
    END AS descricao_tipo
FROM Inventario_Item ii
LEFT JOIN Item i ON ii.id_item = i.id_item
ORDER BY ii.Id_PlayerIn, i.nome;