-- 2.1: Procedure para o jogador comprar do mercante
CREATE OR REPLACE PROCEDURE comprar_item(
  p_player     INT,
  p_mercante   INT,
  p_item       INT,
  p_qtde       INT
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_preco     INT;
  v_custo     INT;
  v_espaco    INT;
BEGIN
  -- 2.1.1: Verifica disponibilidade e bloqueia linha
  SELECT preco_venda, quantidade
    INTO v_preco, v_espaco
    FROM Inventario_Mercante
   WHERE id_mercante = p_mercante
     AND id_item      = p_item
  FOR UPDATE;
  IF NOT FOUND OR v_espaco < p_qtde THEN
    RAISE EXCEPTION 'Item % não disponível no mercante % (sobra %)', p_item, p_mercante, v_espaco;
  END IF;

  -- 2.1.2: Checa saldo do jogador
  v_custo := v_preco * p_qtde;
  IF (SELECT gcs FROM Personagem WHERE id_player = p_player) < v_custo THEN
    RAISE EXCEPTION 'Saldo insuficiente: precisa de %, tem %', v_custo, (SELECT gcs FROM Personagem WHERE id_player = p_player);
  END IF;

  -- 2.1.3: Verifica espaço no inventário do jogador
  SELECT Espaco_Maximo - COALESCE(SUM(Quantidade),0)
    INTO v_espaco
    FROM Inventario_Item
   WHERE Id_PlayerIn = p_player;
  IF v_espaco < p_qtde THEN
    RAISE EXCEPTION 'Espaço insuficiente: só restam %', v_espaco;
  END IF;

  -- 2.1.4: Atualiza Inventario_Item do jogador
  INSERT INTO Inventario_Item (Id_PlayerIn, Id_Item, Quantidade)
    VALUES (p_player, p_item, p_qtde)
  ON CONFLICT (Id_PlayerIn, Id_Item)
    DO UPDATE SET Quantidade = Inventario_Item.Quantidade + EXCLUDED.Quantidade;

  -- 2.1.5: Debita o saldo do jogador
  UPDATE Personagem
     SET gcs = gcs - v_custo
   WHERE id_player = p_player;

  -- 2.1.6: Deduz do estoque do mercante
  UPDATE Inventario_Mercante
     SET quantidade = quantidade - p_qtde
   WHERE id_mercante = p_mercante
     AND id_item      = p_item;
END;
$$;

-- 2.2: Procedure para o jogador vender ao mercante
CREATE OR REPLACE PROCEDURE vender_item(
  p_player     INT,
  p_mercante   INT,
  p_item       INT,
  p_qtde       INT
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_preco   INT;
  v_jogada  INT;
BEGIN
  -- 2.2.1: Verifica se o jogador tem quantidade suficiente
  SELECT Quantidade
    INTO v_jogada
    FROM Inventario_Item
   WHERE Id_PlayerIn = p_player
     AND Id_Item      = p_item
  FOR UPDATE;
  IF NOT FOUND OR v_jogada < p_qtde THEN
    RAISE EXCEPTION 'Jogador não possui % do item %', p_qtde, p_item;
  END IF;

  -- 2.2.2: Busca preço de compra do mercante
  SELECT preco_compra
    INTO v_preco
    FROM Inventario_Mercante
   WHERE id_mercante = p_mercante
     AND id_item      = p_item
  FOR UPDATE;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Mercante % não compra item %', p_mercante, p_item;
  END IF;

  -- 2.2.3: Atualiza Inventario_Item do jogador
  UPDATE Inventario_Item
     SET Quantidade = Quantidade - p_qtde
   WHERE Id_PlayerIn = p_player
     AND Id_Item      = p_item;
  DELETE FROM Inventario_Item
   WHERE Id_PlayerIn = p_player
     AND Id_Item      = p_item
     AND Quantidade   = 0;

  -- 2.2.4: Credita saldo do jogador
  UPDATE Personagem
     SET gcs = gcs + (v_preco * p_qtde)
   WHERE id_player = p_player;

  -- 2.2.5: Reabastece o estoque do mercante
  INSERT INTO Inventario_Mercante (id_mercante, id_item, preco_venda, preco_compra, quantidade)
    VALUES (p_mercante, p_item, (v_preco * 120) / 100, v_preco, p_qtde)
  ON CONFLICT (id_mercante, id_item)
    DO UPDATE SET quantidade = Inventario_Mercante.quantidade + EXCLUDED.quantidade;
END;
$$;
