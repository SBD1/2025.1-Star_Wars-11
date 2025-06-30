-- Cria a tabela de produtos
CREATE TABLE IF NOT EXISTS produto (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  descricao TEXT,
  preco INTEGER NOT NULL,
  quantidade_estoque INTEGER
);

-- Cria a tabela de relação personagem–produto
CREATE TABLE IF NOT EXISTS personagem_produto (
  personagem_id INTEGER NOT NULL
    REFERENCES personagem(id)
    ON DELETE CASCADE,
  produto_id    INTEGER NOT NULL
    REFERENCES produto(id)
    ON DELETE CASCADE,
  quantidade    INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (personagem_id, produto_id)
);
