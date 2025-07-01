-- PROCEDURES - SISTEMA DE LOJA

-- Comprar item de NPC
CREATE OR REPLACE FUNCTION comprar_item(
    p_id_player INT, p_id_npc INT, p_id_item INT, p_quantidade INT DEFAULT 1
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    gcs_jogador INT; preco_item INT; custo_total INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Mercante WHERE id_NPC = p_id_npc) THEN
        RAISE EXCEPTION 'NPC não é mercante';
    END IF;
    
    SELECT gcs INTO gcs_jogador FROM Personagem WHERE id_player = p_id_player;
    SELECT preco INTO preco_item FROM Item WHERE id_item = p_id_item;
    
    custo_total := preco_item * p_quantidade;
    
    IF gcs_jogador < custo_total THEN
        RAISE EXCEPTION 'Créditos insuficientes. Necessário: %, Disponível: %', custo_total, gcs_jogador;
    END IF;
    
    UPDATE Personagem SET gcs = gcs - custo_total WHERE id_player = p_id_player;
    PERFORM adicionar_item(p_id_player, p_id_item, p_quantidade);
    
    RETURN TRUE;
END;
$$;

-- Vender item para NPC
CREATE OR REPLACE FUNCTION vender_item(
    p_id_player INT, p_id_npc INT, p_id_item INT, p_quantidade INT DEFAULT 1
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    id_inv INT; qtd_jogador INT; preco_item INT; valor_venda INT;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Mercante WHERE id_NPC = p_id_npc) THEN
        RAISE EXCEPTION 'NPC não é mercante';
    END IF;
    
    SELECT Id_PlayerIn INTO id_inv FROM Inventario WHERE Id_Player = p_id_player;
    
    SELECT quantidade INTO qtd_jogador 
    FROM Inventario_Item WHERE Id_PlayerIn = id_inv AND id_item = p_id_item;
    
    IF qtd_jogador IS NULL OR qtd_jogador < p_quantidade THEN
        RAISE EXCEPTION 'Quantidade insuficiente';
    END IF;
    
    SELECT preco INTO preco_item FROM Item WHERE id_item = p_id_item;
    valor_venda := (preco_item * p_quantidade) / 2; -- 50% do valor original
    
    PERFORM remover_item(p_id_player, p_id_item, p_quantidade);
    UPDATE Personagem SET gcs = gcs + valor_venda WHERE id_player = p_id_player;
    
    RETURN TRUE;
END;
$$;

-- Consultar preços da loja
CREATE OR REPLACE FUNCTION consultar_loja(p_id_npc INT)
RETURNS TABLE (
    id_item INT, nome_item VARCHAR(50), tipo VARCHAR(20), 
    preco_compra INT, preco_venda INT, disponivel BOOLEAN
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Mercante WHERE id_NPC = p_id_npc) THEN
        RAISE EXCEPTION 'NPC não é mercante';
    END IF;
    
    RETURN QUERY
    SELECT 
        i.id_item,
        i.nome,
        i.tipo,
        i.preco AS preco_compra,
        (i.preco / 2) AS preco_venda,
        TRUE AS disponivel
    FROM Item i
    ORDER BY i.tipo, i.preco;
END;
$$;

-- Verificar poder de compra do jogador
CREATE OR REPLACE FUNCTION poder_compra(p_id_player INT)
RETURNS TABLE (
    id_item INT, nome_item VARCHAR(50), preco INT, 
    pode_comprar BOOLEAN, quantidade_maxima INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    gcs_jogador INT;
BEGIN
    SELECT gcs INTO gcs_jogador FROM Personagem WHERE id_player = p_id_player;
    
    RETURN QUERY
    SELECT 
        i.id_item,
        i.nome,
        i.preco,
        (i.preco <= gcs_jogador) AS pode_comprar,
        (gcs_jogador / i.preco) AS quantidade_maxima
    FROM Item i
    WHERE i.preco <= gcs_jogador
    ORDER BY i.preco;
END;
$$;

-- Histórico de transações (simulado)
CREATE OR REPLACE FUNCTION historico_transacoes(p_id_player INT)
RETURNS TABLE (
    tipo_transacao VARCHAR(10), item VARCHAR(50), quantidade INT, 
    valor INT, data_transacao TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Esta é uma versão simplificada
    -- Em um sistema real, você teria uma tabela de histórico
    RETURN QUERY
    SELECT 
        'COMPRA'::VARCHAR(10) AS tipo_transacao,
        'Exemplo'::VARCHAR(50) AS item,
        1 AS quantidade,
        100 AS valor,
        CURRENT_TIMESTAMP AS data_transacao
    WHERE FALSE; -- Retorna vazio por enquanto
END;
$$;
