-- ========================================
-- DQL - SISTEMA DE COMBATE
-- Consultas úteis para o sistema de combate
-- ========================================

-- 1. VERIFICAR COMBATES ATIVOS
-- Mostra todos os combates que estão acontecendo agora
SELECT 
    c.id_combate,
    c.id_player AS jogador_id,
    i.tipo_mob AS inimigo,
    c.vida_jogador_atual,
    c.vida_inimigo_atual,
    c.turno_atual,
    c.data_inicio,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.data_inicio))/60 AS duracao_minutos
FROM Combate c
JOIN Inimigo i ON c.id_mob = i.id_mob
WHERE c.status_combate = 'ativo'
ORDER BY c.data_inicio DESC;

-- 2. HISTÓRICO DE AÇÕES DE UM COMBATE
-- Substitua o número 1 pelo ID do combate que você quer ver
SELECT 
    cl.turno_numero,
    cl.ator,
    cl.acao,
    cl.dano_causado,
    cl.vida_restante_jogador,
    cl.vida_restante_inimigo,
    cl.descricao_acao,
    cl.timestamp_acao
FROM Combate_Log cl
WHERE cl.id_combate = 1  -- MUDE ESTE NÚMERO
ORDER BY cl.turno_numero, cl.timestamp_acao;

-- 3. RESULTADOS DE COMBATES FINALIZADOS
-- Mostra o histórico de combates já terminados
SELECT 
    cr.id_resultado,
    c.id_player AS jogador_id,
    i.tipo_mob AS inimigo,
    cr.vencedor,
    cr.xp_ganho,
    cr.gcs_ganho,
    cr.total_turnos,
    cr.dano_total_jogador,
    cr.dano_total_inimigo,
    cr.duracao_combate,
    c.data_inicio,
    c.data_fim
FROM Combate_Resultado cr
JOIN Combate c ON cr.id_combate = c.id_combate
JOIN Inimigo i ON c.id_mob = i.id_mob
ORDER BY c.data_fim DESC;

-- 4. ESTATÍSTICAS POR JOGADOR
-- Mostra estatísticas de combate de cada jogador
SELECT
    p.id_player,
    p.nome_classe,
    p.level,
    p.mortes,
    COUNT(*) AS total_combates,
    SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) AS vitorias,
    SUM(CASE WHEN cr.vencedor = 'inimigo' THEN 1 ELSE 0 END) AS derrotas,
    SUM(CASE WHEN cr.vencedor = 'fuga' THEN 1 ELSE 0 END) AS fugas,
    SUM(cr.xp_ganho) AS total_xp_ganho,
    SUM(cr.gcs_ganho) AS total_gcs_ganho,
    ROUND(AVG(cr.total_turnos), 1) AS media_turnos
FROM Combate_Resultado cr
JOIN Combate c ON cr.id_combate = c.id_combate
JOIN Personagem p ON c.id_player = p.id_player
GROUP BY p.id_player, p.nome_classe, p.level, p.mortes
ORDER BY vitorias DESC;

-- 5. INIMIGOS DISPONÍVEIS POR PLANETA
-- Mostra quais inimigos estão em cada planeta
SELECT 
    i.id_mob,
    i.tipo_mob,
    i.vida_base,
    i.nivel,
    i.dano_base,
    i.pontos_escudo,
    i.creditos,
    i.planeta_origem
FROM Inimigo i
ORDER BY i.planeta_origem, i.nivel;

-- 6. STATUS ATUAL DO SISTEMA
-- Visão geral do sistema de combate
SELECT 
    'Combates Ativos' AS categoria,
    COUNT(*)::text AS valor
FROM Combate 
WHERE status_combate = 'ativo'

UNION ALL

SELECT 
    'Combates Finalizados Hoje' AS categoria,
    COUNT(*)::text AS valor
FROM Combate 
WHERE status_combate = 'finalizado' 
  AND DATE(data_fim) = CURRENT_DATE

UNION ALL

SELECT 
    'Total de Inimigos' AS categoria,
    COUNT(*)::text AS valor
FROM Inimigo

UNION ALL

SELECT
    'Jogadores com Combates' AS categoria,
    COUNT(DISTINCT id_player)::text AS valor
FROM Combate

UNION ALL

SELECT
    'Total de Mortes de Jogadores' AS categoria,
    SUM(mortes)::text AS valor
FROM Personagem;
