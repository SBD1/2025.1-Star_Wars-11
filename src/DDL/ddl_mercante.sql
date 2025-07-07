-- 1.1: Tabela de mercantes
CREATE TABLE IF NOT EXISTS Mercante (
  id_mercante   SERIAL PRIMARY KEY,
  nome           TEXT NOT NULL
);

-- 1.2: Estoque de cada mercante
CREATE TABLE IF NOT EXISTS Inventario_Mercante (
  id_mercante   INT NOT NULL
    REFERENCES Mercante(id_mercante)
      ON DELETE CASCADE,
  id_item        INT NOT NULL
    REFERENCES Item(id_Item),
  preco_venda    INT NOT NULL,     -- valor que o mercante cobra
  preco_compra   INT NOT NULL,     -- valor que o mercante paga ao jogador
  quantidade     INT NOT NULL,     -- estoque disponível
  PRIMARY KEY(id_mercante, id_item)
);
