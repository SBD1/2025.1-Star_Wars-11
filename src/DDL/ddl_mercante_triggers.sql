-- 1) Função disparadora que valida estoque e preços
CREATE OR REPLACE FUNCTION trg_check_inventario_mercante()
RETURNS TRIGGER AS $$
BEGIN
  -- Quantidade não pode ser negativa
  IF NEW.quantidade < 0 THEN
    RAISE EXCEPTION 'Quantidade em Inventario_Mercante não pode ser negativa: %', NEW.quantidade;
  END IF;

  -- preco_venda deve ser >= preco_compra
  IF NEW.preco_venda < NEW.preco_compra THEN
    RAISE EXCEPTION 
      'Preco_venda (%) deve ser maior ou igual a preco_compra (%).', 
      NEW.preco_venda, NEW.preco_compra;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2) Trigger que chama a função antes de INSERT ou UPDATE
DROP TRIGGER IF EXISTS trg_check_inventario_mercante 
  ON Inventario_Mercante;
CREATE TRIGGER trg_check_inventario_mercante
  BEFORE INSERT OR UPDATE
  ON Inventario_Mercante
  FOR EACH ROW
  EXECUTE FUNCTION trg_check_inventario_mercante();
