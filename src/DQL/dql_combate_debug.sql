-- ========================================
-- DQL - DEBUG DO SISTEMA DE COMBATE
-- Consultas para identificar problemas
-- ========================================

-- 🎯 HISTÓRICO COMPLETO DE COMBATES POR JOGADOR
-- Mostra todos os combates de todos os jogadores com resultado
SELECT
    p.id_player,
    p.nome_classe,
    p.level,
    p.mortes,
    i.tipo_mob AS inimigo_enfrentado,
    i.nivel AS nivel_inimigo,
    cr.vencedor,
    CASE
        WHEN cr.vencedor = 'jogador' THEN '🏆 VITÓRIA'
        WHEN cr.vencedor = 'inimigo' THEN '💀 DERROTA'
        ELSE '🏃 FUGA'
    END AS resultado,
    cr.xp_ganho,
    cr.gcs_ganho,
    cr.total_turnos,
    cr.duracao_combate,
    c.data_inicio
FROM Combate c
JOIN Personagem p ON c.id_player = p.id_player
JOIN Inimigo i ON c.id_mob = i.id_mob
JOIN Combate_Resultado cr ON c.id_combate = cr.id_combate
ORDER BY p.id_player, c.data_inicio DESC;

-- 📊 RESUMO DE COMBATES POR JOGADOR
-- Estatísticas consolidadas de cada jogador
SELECT
    p.id_player,
    p.nome_classe,
    p.level,
    p.mortes,
    COUNT(*) AS total_combates,
    SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) AS vitorias,
    SUM(CASE WHEN cr.vencedor = 'inimigo' THEN 1 ELSE 0 END) AS derrotas,
    SUM(CASE WHEN cr.vencedor = 'fuga' THEN 1 ELSE 0 END) AS fugas,
    ROUND(
        (SUM(CASE WHEN cr.vencedor = 'jogador' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 1
    ) AS taxa_vitoria_pct,
    SUM(cr.xp_ganho) AS total_xp_ganho,
    SUM(cr.gcs_ganho) AS total_gcs_ganho
FROM Combate c
JOIN Personagem p ON c.id_player = p.id_player
JOIN Combate_Resultado cr ON c.id_combate = cr.id_combate
GROUP BY p.id_player, p.nome_classe, p.level, p.mortes
ORDER BY vitorias DESC, total_combates DESC;

-- 1. VERIFICAR INTEGRIDADE DOS DADOS
-- Procura por inconsistências no sistema
SELECT 
    'Combates sem log' AS problema,
    COUNT(*) AS quantidade
FROM Combate c
LEFT JOIN Combate_Log cl ON c.id_combate = cl.id_combate
WHERE cl.id_combate IS NULL

UNION ALL

SELECT 
    'Combates finalizados sem resultado' AS problema,
    COUNT(*) AS quantidade
FROM Combate c
LEFT JOIN Combate_Resultado cr ON c.id_combate = cr.id_combate
WHERE c.status_combate = 'finalizado' AND cr.id_combate IS NULL

UNION ALL

SELECT 
    'Combates ativos há mais de 1 hora' AS problema,
    COUNT(*) AS quantidade
FROM Combate c
WHERE c.status_combate = 'ativo' 
  AND c.data_inicio < CURRENT_TIMESTAMP - INTERVAL '1 hour';

-- 2. VERIFICAR ESTRUTURA DAS TABELAS
-- Mostra a estrutura das tabelas de combate
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name IN ('combate', 'combate_log', 'combate_resultado')
ORDER BY table_name, ordinal_position;

-- 3. VERIFICAR CONSTRAINTS E ÍNDICES
-- Mostra as restrições das tabelas de combate
SELECT 
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu 
    ON tc.constraint_name = kcu.constraint_name
WHERE tc.table_name IN ('combate', 'combate_log', 'combate_resultado')
ORDER BY tc.table_name, tc.constraint_type;

-- 4. ÚLTIMOS ERROS DE COMBATE
-- Procura por logs com problemas
SELECT 
    cl.id_log,
    cl.id_combate,
    cl.ator,
    cl.acao,
    cl.descricao_acao,
    cl.timestamp_acao
FROM Combate_Log cl
WHERE cl.descricao_acao LIKE '%Erro%' 
   OR cl.descricao_acao LIKE '%erro%'
   OR cl.dano_causado < 0
ORDER BY cl.timestamp_acao DESC
LIMIT 10;

-- 5. COMBATES ÓRFÃOS
-- Combates que referenciam jogadores ou inimigos inexistentes
SELECT 
    'Combates com jogador inexistente' AS problema,
    COUNT(*) AS quantidade
FROM Combate c
LEFT JOIN Personagem p ON c.id_player = p.id_player
WHERE p.id_player IS NULL

UNION ALL

SELECT 
    'Combates com inimigo inexistente' AS problema,
    COUNT(*) AS quantidade
FROM Combate c
LEFT JOIN Inimigo i ON c.id_mob = i.id_mob
WHERE i.id_mob IS NULL;

-- 6. LIMPEZA DE COMBATES ANTIGOS (APENAS VISUALIZAR)
-- Mostra combates que poderiam ser limpos
SELECT 
    c.id_combate,
    c.id_player,
    c.status_combate,
    c.data_inicio,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - c.data_inicio))/3600 AS horas_ativo
FROM Combate c
WHERE c.status_combate = 'ativo' 
  AND c.data_inicio < CURRENT_TIMESTAMP - INTERVAL '2 hours'
ORDER BY c.data_inicio;

-- COMANDO PARA LIMPAR (DESCOMENTE APENAS SE NECESSÁRIO):
-- DELETE FROM Combate WHERE status_combate = 'ativo' AND data_inicio < CURRENT_TIMESTAMP - INTERVAL '2 hours';
