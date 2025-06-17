-- Seleciona todos os mobs com nível de ameaça maior que 5
SELECT *
FROM MOB
WHERE nivel_ameaca > 5;

-- Seleciona o id, vida base e tipo de mob de todos os inimigos
SELECT id_mob, vida_base, tipo_mob
FROM Inimigo;

-- Seleciona inimigos com vida base menor que 150 e nível maior ou igual a 3
SELECT *
FROM Inimigo
WHERE vida_base < 150 AND nivel >= 3;

-- Seleciona inimigos do planeta 'Terra' e ordena pelo nível em ordem decrescente
SELECT *
FROM Inimigo
WHERE planeta_origem = 'Terra'
ORDER BY nivel DESC;

-- Junta as tabelas Inimigo e MOB para mostrar o tipo de mob e seu nível de ameaça
SELECT I.id_mob, I.tipo_mob, M.nivel_ameaca, I.planeta_origem
FROM Inimigo AS I
JOIN MOB AS M ON I.tipo_mob = M.tipo_mob;

-- Seleciona inimigos que são do tipo 'Normal' e têm Formação Tática
SELECT I.id_mob, I.tipo_mob, N.Formacao_Tatica
FROM Inimigo AS I
JOIN Normal AS N ON I.tipo_mob = N.tipo_mob
WHERE N.Formacao_Tatica = TRUE;

-- Seleciona inimigos que são do tipo 'Elite' e têm Armadura Reforçada
SELECT I.id_mob, I.tipo_mob, E.Armadura_Reforçada
FROM Inimigo AS I
JOIN Elite AS E ON I.tipo_mob = E.tipo_mob
WHERE E.Armadura_Reforçada = TRUE;

-- Seleciona inimigos que são do tipo 'Boss' e mostra seu Arsenal
SELECT I.id_mob, I.tipo_mob, B.Arsenal
FROM Inimigo AS I
JOIN Boss AS B ON I.tipo_mob = B.tipo_mob;

-- Conta quantos inimigos existem para cada tipo de mob
SELECT tipo_mob, COUNT(id_mob) AS total_inimigos
FROM Inimigo
GROUP BY tipo_mob;

-- Encontra todos os itens no inventário de um inimigo específico (ex: id_mob = 1)
SELECT IA.item, IA.quantidade, IA.raridade
FROM Inventario_IA AS IA
WHERE IA.id_mob = 1;

-- Lista todos os inimigos e os itens em seus inventários (se houver)
SELECT I.id_mob, I.tipo_mob, IA.item, IA.quantidade, IA.raridade
FROM Inimigo AS I
LEFT JOIN Inventario_IA AS IA ON I.id_mob = IA.id_mob;

-- Seleciona mobs que são do tipo 'Normal' e que patrulham
SELECT M.tipo_mob, M.nivel_ameaca, N.Patrulha
FROM MOB AS M
JOIN Normal AS N ON M.tipo_mob = N.tipo_mob
WHERE N.Patrulha = TRUE;
