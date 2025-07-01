-- PROCEDURES - GESTÃO DE INVENTÁRIO

-- Adicionar item ao inventário
CREATE OR REPLACE FUNCTION adicionar_item(
    p_id_player INT,
    p_id_item INT,
    p_quantidade INT DEFAULT 1
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    id_inventario INT;
    peso_item INT;
    peso_atual INT;
    espaco_max INT;
BEGIN
    SELECT Id_PlayerIn, Peso_Total, Espaco_Maximo
    INTO id_inventario, peso_atual, espaco_max
    FROM Inventario WHERE Id_Player = p_id_player;
    
    SELECT Peso INTO peso_item FROM Item WHERE id_item = p_id_item;
    
    IF id_inventario IS NULL OR peso_item IS NULL THEN
        RAISE EXCEPTION 'Jogador ou item não encontrado';
    END IF;
    
    IF (peso_atual + peso_item * p_quantidade) > espaco_max THEN
        RAISE EXCEPTION 'Inventário cheio';
    END IF;
    
    INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade)
    VALUES (id_inventario, p_id_item, p_quantidade)
    ON CONFLICT (Id_PlayerIn, id_item) 
    DO UPDATE SET quantidade = Inventario_Item.quantidade + p_quantidade;
    
    UPDATE Inventario 
    SET Peso_Total = peso_atual + (peso_item * p_quantidade)
    WHERE Id_PlayerIn = id_inventario;
    
    RETURN TRUE;
END;
$$;

-- Remover item do inventário
CREATE OR REPLACE FUNCTION remover_item(
    p_id_player INT,
    p_id_item INT,
    p_quantidade INT DEFAULT 1
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    id_inventario INT;
    qtd_atual INT;
    peso_item INT;
BEGIN
    SELECT Id_PlayerIn INTO id_inventario 
    FROM Inventario WHERE Id_Player = p_id_player;
    
    SELECT quantidade INTO qtd_atual 
    FROM Inventario_Item 
    WHERE Id_PlayerIn = id_inventario AND id_item = p_id_item;
    
    SELECT Peso INTO peso_item FROM Item WHERE id_item = p_id_item;
    
    IF qtd_atual IS NULL OR qtd_atual < p_quantidade THEN
        RAISE EXCEPTION 'Quantidade insuficiente';
    END IF;
    
    IF qtd_atual = p_quantidade THEN
        DELETE FROM Inventario_Item 
        WHERE Id_PlayerIn = id_inventario AND id_item = p_id_item;
    ELSE
        UPDATE Inventario_Item 
        SET quantidade = quantidade - p_quantidade
        WHERE Id_PlayerIn = id_inventario AND id_item = p_id_item;
    END IF;
    
    UPDATE Inventario 
    SET Peso_Total = Peso_Total - (peso_item * p_quantidade)
    WHERE Id_PlayerIn = id_inventario;
    
    RETURN TRUE;
END;
$$;

-- Trocar itens entre jogadores
CREATE OR REPLACE FUNCTION trocar_itens(
    p_origem INT, p_destino INT, p_id_item INT, p_quantidade INT
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    inv_origem INT; inv_destino INT; qtd_origem INT; peso_item INT;
BEGIN
    SELECT Id_PlayerIn INTO inv_origem FROM Inventario WHERE Id_Player = p_origem;
    SELECT Id_PlayerIn INTO inv_destino FROM Inventario WHERE Id_Player = p_destino;
    
    SELECT quantidade INTO qtd_origem 
    FROM Inventario_Item WHERE Id_PlayerIn = inv_origem AND id_item = p_id_item;
    
    SELECT Peso INTO peso_item FROM Item WHERE id_item = p_id_item;
    
    IF qtd_origem < p_quantidade THEN
        RAISE EXCEPTION 'Quantidade insuficiente';
    END IF;
    
    -- Verificar espaço no destino
    IF (SELECT Peso_Total + (peso_item * p_quantidade) FROM Inventario WHERE Id_PlayerIn = inv_destino) >
       (SELECT Espaco_Maximo FROM Inventario WHERE Id_PlayerIn = inv_destino) THEN
        RAISE EXCEPTION 'Inventário destino cheio';
    END IF;
    
    -- Transferir
    UPDATE Inventario_Item SET quantidade = quantidade - p_quantidade
    WHERE Id_PlayerIn = inv_origem AND id_item = p_id_item;
    
    DELETE FROM Inventario_Item 
    WHERE Id_PlayerIn = inv_origem AND id_item = p_id_item AND quantidade = 0;
    
    INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade)
    VALUES (inv_destino, p_id_item, p_quantidade)
    ON CONFLICT (Id_PlayerIn, id_item) 
    DO UPDATE SET quantidade = Inventario_Item.quantidade + p_quantidade;
    
    -- Atualizar pesos
    UPDATE Inventario SET Peso_Total = Peso_Total - (peso_item * p_quantidade) WHERE Id_PlayerIn = inv_origem;
    UPDATE Inventario SET Peso_Total = Peso_Total + (peso_item * p_quantidade) WHERE Id_PlayerIn = inv_destino;
    
    RETURN TRUE;
END;
$$;

-- Consultar inventário
CREATE OR REPLACE FUNCTION consultar_inventario(p_id_player INT)
RETURNS TABLE (
    nome_item VARCHAR(50), tipo VARCHAR(20), quantidade INT, 
    peso_unitario INT, peso_total INT, valor_unitario INT, valor_total INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome, i.tipo, ii.quantidade,
        i.Peso, (i.Peso * ii.quantidade),
        i.preco, (i.preco * ii.quantidade)
    FROM Inventario inv
    JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
    JOIN Item i ON ii.id_item = i.id_item
    WHERE inv.Id_Player = p_id_player
    ORDER BY i.tipo, i.nome;
END;
$$;
