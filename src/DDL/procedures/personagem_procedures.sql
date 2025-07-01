-- PROCEDURES - GESTÃO DE PERSONAGENS

-- Criar novo personagem
CREATE OR REPLACE FUNCTION novo_personagem(
    p_nome_classe VARCHAR(22),
    p_nome_planeta VARCHAR(20),
    p_dano_base INT DEFAULT 10
)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    novo_id INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Classe WHERE nome_classe = p_nome_classe) THEN
        RAISE EXCEPTION 'Classe % não existe', p_nome_classe;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM Planeta WHERE nome_planeta = p_nome_planeta) THEN
        RAISE EXCEPTION 'Planeta % não existe', p_nome_planeta;
    END IF;
    
    INSERT INTO Personagem (dano_base, nome_classe, nome_planeta)
    VALUES (p_dano_base, p_nome_classe, p_nome_planeta)
    RETURNING id_player INTO novo_id;
    
    RETURN novo_id;
END;
$$;

-- Sistema de level up
CREATE OR REPLACE FUNCTION subir_level(p_id_player INT)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    xp_atual INT;
    level_atual INT;
    novo_level INT;
BEGIN
    SELECT xp, level INTO xp_atual, level_atual
    FROM Personagem WHERE id_player = p_id_player;
    
    novo_level := (xp_atual / 1000) + 1;
    
    IF novo_level > level_atual THEN
        UPDATE Personagem 
        SET level = novo_level,
            vida_base = vida_base + ((novo_level - level_atual) * 20),
            dano_base = dano_base + ((novo_level - level_atual) * 5)
        WHERE id_player = p_id_player;
        RETURN TRUE;
    END IF;
    
    RETURN FALSE;
END;
$$;

-- Status completo do personagem
CREATE OR REPLACE FUNCTION status_personagem(p_id_player INT)
RETURNS TABLE (
    id_player INT, level INT, vida_base INT, dano_base INT, xp INT, gcs INT,
    nome_classe VARCHAR(22), nome_planeta VARCHAR(20), determinacao INT,
    total_naves BIGINT, missoes_concluidas BIGINT, total_itens BIGINT, valor_inventario BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id_player, p.level, p.vida_base, p.dano_base, p.xp, p.gcs,
        p.nome_classe, p.nome_planeta, c.Determinacao,
        COUNT(DISTINCT n.modelo) AS total_naves,
        COUNT(CASE WHEN mj.status_jogador = 'Concluída' THEN 1 END) AS missoes_concluidas,
        COALESCE(SUM(ii.quantidade), 0) AS total_itens,
        COALESCE(SUM(i.preco * ii.quantidade), 0) AS valor_inventario
    FROM Personagem p
    LEFT JOIN Classe c ON p.nome_classe = c.nome_classe
    LEFT JOIN Nave n ON p.id_player = n.Id_Player
    LEFT JOIN Missao_Jogador mj ON p.id_player = mj.id_player
    LEFT JOIN Inventario inv ON p.id_player = inv.Id_Player
    LEFT JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
    LEFT JOIN Item i ON ii.id_item = i.id_item
    WHERE p.id_player = p_id_player
    GROUP BY p.id_player, p.level, p.vida_base, p.dano_base, p.xp, p.gcs, 
             p.nome_classe, p.nome_planeta, c.Determinacao;
END;
$$;

-- Ranking de poder
CREATE OR REPLACE FUNCTION ranking_poder()
RETURNS TABLE (
    posicao INT, id_player INT, nome_classe VARCHAR(22), 
    level INT, poder_total INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ROW_NUMBER() OVER (ORDER BY (p.level * 10 + p.vida_base + p.dano_base) DESC)::INT AS posicao,
        p.id_player,
        p.nome_classe,
        p.level,
        (p.level * 10 + p.vida_base + p.dano_base) AS poder_total
    FROM Personagem p
    ORDER BY poder_total DESC;
END;
$$;
