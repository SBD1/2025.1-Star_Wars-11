-- PROCEDURES - ADMINISTRAÇÃO E RELATÓRIOS

-- Estatísticas gerais do servidor
CREATE OR REPLACE FUNCTION relatorio_servidor()
RETURNS TABLE (
    total_jogadores BIGINT, total_missoes BIGINT, missoes_concluidas BIGINT,
    total_itens BIGINT, creditos_economia BIGINT, jogador_top INT, planeta_popular VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM Personagem),
        (SELECT COUNT(*) FROM Missao),
        (SELECT COUNT(*) FROM Missao_Jogador WHERE status_jogador = 'Concluída'),
        (SELECT COALESCE(SUM(quantidade), 0) FROM Inventario_Item),
        (SELECT COALESCE(SUM(gcs), 0) FROM Personagem),
        (SELECT id_player FROM Personagem ORDER BY (level * 10 + vida_base + dano_base) DESC LIMIT 1),
        (SELECT nome_planeta FROM Personagem GROUP BY nome_planeta ORDER BY COUNT(*) DESC LIMIT 1);
END;
$$;

-- Relatório de atividade por planeta
CREATE OR REPLACE FUNCTION atividade_planetas()
RETURNS TABLE (
    nome_planeta VARCHAR(20), total_jogadores BIGINT, total_missoes BIGINT,
    total_npcs BIGINT, total_inimigos BIGINT, nivel_atividade VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.nome_planeta,
        COUNT(DISTINCT pe.id_player) AS total_jogadores,
        COUNT(DISTINCT m.id_missao) AS total_missoes,
        COUNT(DISTINCT n.id_NPC) AS total_npcs,
        COUNT(DISTINCT i.id_mob) AS total_inimigos,
        CASE 
            WHEN COUNT(DISTINCT pe.id_player) > 2 THEN 'Alto'
            WHEN COUNT(DISTINCT pe.id_player) > 0 THEN 'Médio'
            ELSE 'Baixo'
        END AS nivel_atividade
    FROM Planeta p
    LEFT JOIN Personagem pe ON p.nome_planeta = pe.nome_planeta
    LEFT JOIN Missao m ON p.nome_planeta = m.nome_planeta
    LEFT JOIN Npc n ON p.nome_planeta = n.nome_planeta
    LEFT JOIN Inimigo i ON p.nome_planeta = i.planeta_origem
    GROUP BY p.nome_planeta
    ORDER BY total_jogadores DESC, total_missoes DESC;
END;
$$;

-- Top jogadores por diferentes critérios
CREATE OR REPLACE FUNCTION top_jogadores(p_criterio VARCHAR(20) DEFAULT 'poder')
RETURNS TABLE (
    posicao INT, id_player INT, nome_classe VARCHAR(22), 
    level INT, valor INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    CASE p_criterio
        WHEN 'poder' THEN
            RETURN QUERY
            SELECT 
                ROW_NUMBER() OVER (ORDER BY (p.level * 10 + p.vida_base + p.dano_base) DESC)::INT,
                p.id_player, p.nome_classe, p.level,
                (p.level * 10 + p.vida_base + p.dano_base) AS valor
            FROM Personagem p
            ORDER BY valor DESC
            LIMIT 10;
            
        WHEN 'level' THEN
            RETURN QUERY
            SELECT 
                ROW_NUMBER() OVER (ORDER BY p.level DESC, p.xp DESC)::INT,
                p.id_player, p.nome_classe, p.level,
                p.level AS valor
            FROM Personagem p
            ORDER BY p.level DESC, p.xp DESC
            LIMIT 10;
            
        WHEN 'creditos' THEN
            RETURN QUERY
            SELECT 
                ROW_NUMBER() OVER (ORDER BY p.gcs DESC)::INT,
                p.id_player, p.nome_classe, p.level,
                p.gcs AS valor
            FROM Personagem p
            ORDER BY p.gcs DESC
            LIMIT 10;
            
        WHEN 'xp' THEN
            RETURN QUERY
            SELECT 
                ROW_NUMBER() OVER (ORDER BY p.xp DESC)::INT,
                p.id_player, p.nome_classe, p.level,
                p.xp AS valor
            FROM Personagem p
            ORDER BY p.xp DESC
            LIMIT 10;
    END CASE;
END;
$$;

-- Análise de economia do jogo
CREATE OR REPLACE FUNCTION analise_economia()
RETURNS TABLE (
    categoria VARCHAR(30), total_creditos BIGINT, media_creditos NUMERIC,
    quantidade BIGINT, percentual NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    total_economia BIGINT;
BEGIN
    SELECT COALESCE(SUM(gcs), 0) + COALESCE(SUM(i.preco * ii.quantidade), 0)
    INTO total_economia
    FROM Personagem p
    FULL OUTER JOIN Inventario inv ON p.id_player = inv.Id_Player
    FULL OUTER JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
    FULL OUTER JOIN Item i ON ii.id_item = i.id_item;
    
    RETURN QUERY
    SELECT 
        'Créditos em Carteira'::VARCHAR(30),
        COALESCE(SUM(p.gcs), 0),
        COALESCE(AVG(p.gcs), 0),
        COUNT(p.id_player),
        CASE WHEN total_economia > 0 THEN (COALESCE(SUM(p.gcs), 0) * 100.0 / total_economia) ELSE 0 END
    FROM Personagem p
    
    UNION ALL
    
    SELECT 
        'Valor em Inventários'::VARCHAR(30),
        COALESCE(SUM(i.preco * ii.quantidade), 0),
        COALESCE(AVG(i.preco * ii.quantidade), 0),
        COUNT(DISTINCT ii.Id_PlayerIn),
        CASE WHEN total_economia > 0 THEN (COALESCE(SUM(i.preco * ii.quantidade), 0) * 100.0 / total_economia) ELSE 0 END
    FROM Inventario_Item ii
    JOIN Item i ON ii.id_item = i.id_item
    
    UNION ALL
    
    SELECT 
        'Recompensas Pendentes'::VARCHAR(30),
        COALESCE(SUM(m.valor_recompensa), 0),
        COALESCE(AVG(m.valor_recompensa), 0),
        COUNT(m.id_missao),
        CASE WHEN total_economia > 0 THEN (COALESCE(SUM(m.valor_recompensa), 0) * 100.0 / total_economia) ELSE 0 END
    FROM Missao m
    WHERE m.status = 'Disponível';
END;
$$;

-- Limpeza de dados (CUIDADO!)
CREATE OR REPLACE FUNCTION limpar_dados_teste()
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    resultado TEXT := '';
BEGIN
    -- ATENÇÃO: Esta função remove dados de teste!
    -- Use apenas em ambiente de desenvolvimento
    
    DELETE FROM Missao_Jogador;
    resultado := resultado || 'Missões de jogadores removidas. ';
    
    DELETE FROM Inventario_Item;
    resultado := resultado || 'Itens de inventário removidos. ';
    
    UPDATE Inventario SET Peso_Total = 0;
    resultado := resultado || 'Peso dos inventários resetado. ';
    
    UPDATE Personagem SET xp = 0, gcs = 1000, level = 1;
    resultado := resultado || 'Stats dos personagens resetados. ';
    
    RETURN resultado || 'Limpeza concluída!';
END;
$$;

-- Backup de estatísticas importantes
CREATE OR REPLACE FUNCTION backup_stats()
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    stats JSON;
BEGIN
    SELECT json_build_object(
        'timestamp', CURRENT_TIMESTAMP,
        'total_jogadores', (SELECT COUNT(*) FROM Personagem),
        'total_missoes_concluidas', (SELECT COUNT(*) FROM Missao_Jogador WHERE status_jogador = 'Concluída'),
        'economia_total', (SELECT COALESCE(SUM(gcs), 0) FROM Personagem),
        'level_medio', (SELECT COALESCE(AVG(level), 0) FROM Personagem),
        'jogador_mais_forte', (SELECT id_player FROM Personagem ORDER BY (level * 10 + vida_base + dano_base) DESC LIMIT 1)
    ) INTO stats;
    
    RETURN stats;
END;
$$;
