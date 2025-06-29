-- ========================================
-- CONSULTAS DQL - MOBS E INIMIGOS
-- ========================================

-- 1. Seleciona todos os mobs com nível de ameaça maior que 5
SELECT tipo_mob, nivel_ameaca
FROM MOB
WHERE nivel_ameaca > 5
ORDER BY nivel_ameaca DESC;

-- 2. Seleciona informações básicas de todos os inimigos
SELECT id_mob, vida_base, nivel, dano_base, tipo_mob, planeta_origem
FROM Inimigo
ORDER BY nivel DESC, vida_base DESC;

-- 3. Seleciona inimigos com vida base menor que 150 e nível maior ou igual a 3
SELECT id_mob, vida_base, nivel, tipo_mob, planeta_origem
FROM Inimigo
WHERE vida_base < 150 AND nivel >= 3
ORDER BY nivel DESC;

-- 4. Seleciona inimigos de um planeta específico (exemplo: Tatooine)
SELECT id_mob, vida_base, nivel, dano_base, tipo_mob
FROM Inimigo
WHERE planeta_origem = 'Tatooine'
ORDER BY nivel DESC;

-- 5. Junta as tabelas Inimigo e MOB para mostrar informações completas
SELECT I.id_mob, I.vida_base, I.nivel, I.tipo_mob, M.nivel_ameaca, I.planeta_origem
FROM Inimigo I
INNER JOIN MOB M ON I.tipo_mob = M.tipo_mob
ORDER BY M.nivel_ameaca DESC, I.nivel DESC;

-- 6. Seleciona inimigos do tipo 'Normal' com suas características específicas
SELECT I.id_mob, I.tipo_mob, I.nivel, N.Formacao_Tatica, N.Patrulha, N.Ataque_Coordenado
FROM Inimigo I
INNER JOIN Normal N ON I.tipo_mob = N.tipo_mob
ORDER BY I.nivel DESC;

-- 7. Seleciona inimigos do tipo 'Elite' com suas características específicas
SELECT I.id_mob, I.tipo_mob, I.nivel, E.Armadura_Reforçada, E.Ataque_Especial, E.Regeneracao
FROM Inimigo I
INNER JOIN Elite E ON I.tipo_mob = E.tipo_mob
ORDER BY I.nivel DESC;

-- 8. Seleciona inimigos do tipo 'Boss' com suas características específicas
SELECT I.id_mob, I.tipo_mob, I.nivel, B.Arsenal, B.Habilidade_Unica, B.Invocacao_Aliados
FROM Inimigo I
INNER JOIN Boss B ON I.tipo_mob = B.tipo_mob
ORDER BY I.nivel DESC;

-- 9. Conta quantos inimigos existem para cada tipo de mob
SELECT tipo_mob, COUNT(*) AS total_inimigos, AVG(nivel) AS nivel_medio
FROM Inimigo
GROUP BY tipo_mob
ORDER BY total_inimigos DESC;

-- 10. Lista itens no inventário de um inimigo específico
SELECT IA.id_mob, I.tipo_mob, IA.item, IA.quantidade, IA.raridade
FROM Inventario_IA IA
INNER JOIN Inimigo I ON IA.id_mob = I.id_mob
WHERE IA.id_mob = 1;

-- 11. Lista todos os inimigos e seus inventários (incluindo os sem itens)
SELECT I.id_mob, I.tipo_mob, I.nivel,
       COALESCE(IA.item, 'Sem itens') AS item,
       COALESCE(IA.quantidade, 0) AS quantidade,
       COALESCE(IA.raridade, 'N/A') AS raridade
FROM Inimigo I
LEFT JOIN Inventario_IA IA ON I.id_mob = IA.id_mob
ORDER BY I.id_mob, IA.item;

-- 12. Estatísticas por tipo de mob
SELECT M.tipo_mob, M.nivel_ameaca,
       COUNT(I.id_mob) AS total_inimigos,
       AVG(I.vida_base) AS vida_media,
       AVG(I.nivel) AS nivel_medio,
       MAX(I.dano_base) AS maior_dano
FROM MOB M
LEFT JOIN Inimigo I ON M.tipo_mob = I.tipo_mob
GROUP BY M.tipo_mob, M.nivel_ameaca
ORDER BY M.nivel_ameaca DESC;
