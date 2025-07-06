CREATE OR REPLACE FUNCTION adicionar_item_inventario(
    jogador_id INT, 
    item_id_add INT, 
    quantidade_add INT
)
RETURNS TEXT AS $$
DECLARE
    inventario_id INT;
    item_existente INT;
BEGIN
    SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = jogador_id;
    IF NOT FOUND THEN RETURN 'Erro: Inventário do jogador não encontrado.'; END IF;
    SELECT quantidade INTO item_existente FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_add;
    IF FOUND THEN
        UPDATE Inventario_Item SET quantidade = quantidade + quantidade_add WHERE Id_PlayerIn = inventario_id AND id_item = item_id_add;
    ELSE
        INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade) VALUES (inventario_id, item_id_add, quantidade_add);
    END IF;
    RETURN (SELECT nome FROM Item WHERE id_item = item_id_add) || ' (x' || quantidade_add || ') adicionado ao inventário.';
END;
$$ LANGUAGE plpgsql;


-- Nenhuma mudança necessária nesta função.
CREATE OR REPLACE FUNCTION listar_inventario_jogador(jogador_id INT)
RETURNS TABLE (
    id_item INT, nome_item VARCHAR(50), quantidade INT, tipo_item VARCHAR(20), peso_item INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT i.id_item, i.nome, ii.quantidade, i.tipo, i.Peso
    FROM Inventario inv
    JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn
    JOIN Item i ON ii.id_item = i.id_item
    WHERE inv.Id_Player = jogador_id
    ORDER BY i.nome;
END;
$$ LANGUAGE plpgsql;


-- *** MUDANÇA PRINCIPAL APLICADA AQUI ***
CREATE OR REPLACE FUNCTION usar_item_inventario(
    jogador_id INT, 
    item_id_usar INT
)
RETURNS TEXT AS $$
DECLARE
    inventario_id INT;
    item_info RECORD;
    quantidade_atual INT;
    vida_maxima INT; -- Variável para guardar a vida base (máxima)
BEGIN
    SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = jogador_id;
    SELECT quantidade INTO quantidade_atual FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar;
    IF NOT FOUND OR quantidade_atual <= 0 THEN
        RETURN 'Você não possui este item.';
    END IF;

    SELECT nome, efeito_tipo, efeito_valor INTO item_info FROM Item WHERE id_item = item_id_usar;

    CASE item_info.efeito_tipo
        WHEN 'CURA_VIDA' THEN
            -- CORREÇÃO: Buscamos a vida_base para usar como teto da cura.
            SELECT vida_base INTO vida_maxima FROM Personagem WHERE id_player = jogador_id;

            -- CORREÇÃO: Atualizamos a 'vida_atual' do personagem, não a 'vida_base'.
            -- A função LEAST garante que a vida atual não ultrapasse a vida máxima.
            UPDATE Personagem
            SET vida_atual = LEAST(vida_maxima, vida_atual + item_info.efeito_valor)
            WHERE id_player = jogador_id;
        ELSE
            RETURN 'Este item não pode ser usado.';
    END CASE;

    IF quantidade_atual > 1 THEN
        UPDATE Inventario_Item SET quantidade = quantidade - 1 WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar;
    ELSE
        DELETE FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar;
    END IF;
    
    RETURN 'Você usou ' || item_info.nome || '. Sua vida foi restaurada!';
END;
$$ LANGUAGE plpgsql;


-- Nenhuma mudança necessária nesta função.
CREATE OR REPLACE FUNCTION administrar_adicionar_item(
    p_player_id INT,
    p_item_name TEXT,
    p_quantity INT
)
RETURNS TEXT AS $$
DECLARE
    v_item_id INT;
    v_result_text TEXT;
BEGIN
    SELECT id_item INTO v_item_id FROM Item WHERE nome = p_item_name;
    IF NOT FOUND THEN
        RETURN 'ERRO: Item com o nome "' || p_item_name || '" não foi encontrado.';
    END IF;
    SELECT adicionar_item_inventario(p_player_id, v_item_id, p_quantity) INTO v_result_text;
    RETURN v_result_text;
END;
$$ LANGUAGE plpgsql;
