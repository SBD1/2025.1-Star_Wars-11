-- ========================================
-- CONSULTAS DQL - INVENTÁRIO E ITENS
-- ========================================

-- 1. Lista todos os itens no inventário dos jogadores
SELECT
    inv.Id_Player,
    ii.Id_PlayerIn,
    i.nome AS nome_item,
    i.tipo,
    i.peso,
    i.preco,
    ii.quantidade,
    (i.peso * ii.quantidade) AS peso_total_item,
    (i.preco * ii.quantidade) AS valor_total_item,
    CASE
        WHEN i.tipo = 'arma' THEN 'Item de Ataque'
        WHEN i.tipo = 'armadura' THEN 'Item de Defesa'
        WHEN i.tipo = 'consumivel' THEN 'Item de Uso Temporário'
        WHEN i.tipo = 'especial' THEN 'Item Especial'
        ELSE 'Outro Tipo'
    END AS descricao_tipo
FROM Inventario_Item ii
INNER JOIN Item i ON ii.id_item = i.id_item
INNER JOIN Inventario inv ON ii.Id_PlayerIn = inv.Id_PlayerIn
ORDER BY inv.Id_Player, i.nome;

-- 2. Resumo do inventário por jogador
SELECT
    inv.Id_Player,
    inv.Espaco_Maximo,
    inv.Peso_Total,
    COUNT(ii.id_item) AS total_tipos_itens,
    SUM(ii.quantidade) AS total_itens,
    SUM(i.peso * ii.quantidade) AS peso_calculado,
    SUM(i.preco * ii.quantidade) AS valor_total_inventario
FROM Inventario inv
LEFT JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
LEFT JOIN Item i ON ii.id_item = i.id_item
GROUP BY inv.Id_Player, inv.Id_PlayerIn, inv.Espaco_Maximo, inv.Peso_Total
ORDER BY inv.Id_Player;

-- 3. Itens por tipo
SELECT
    i.tipo,
    COUNT(*) AS total_itens_tipo,
    AVG(i.peso) AS peso_medio,
    AVG(i.preco) AS preco_medio,
    MIN(i.preco) AS preco_minimo,
    MAX(i.preco) AS preco_maximo
FROM Item i
GROUP BY i.tipo
ORDER BY total_itens_tipo DESC;

-- 4. Jogadores com inventário mais valioso
SELECT
    inv.Id_Player,
    COUNT(ii.id_item) AS tipos_diferentes,
    SUM(ii.quantidade) AS total_itens,
    SUM(i.preco * ii.quantidade) AS valor_total
FROM Inventario inv
INNER JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
INNER JOIN Item i ON ii.id_item = i.id_item
GROUP BY inv.Id_Player
ORDER BY valor_total DESC;

-- 5. Itens mais populares (mais presentes nos inventários)
SELECT
    i.nome,
    i.tipo,
    i.preco,
    COUNT(ii.Id_PlayerIn) AS jogadores_que_possuem,
    SUM(ii.quantidade) AS quantidade_total
FROM Item i
INNER JOIN Inventario_Item ii ON i.id_item = ii.id_item
GROUP BY i.id_item, i.nome, i.tipo, i.preco
ORDER BY jogadores_que_possuem DESC, quantidade_total DESC;