-- Criação das tabelas relacionadas ao Inventário do Jogador

-- Tabela Inventário do Jogador
CREATE TABLE Inventario (
    Id_PlayerIn INT PRIMARY KEY,
    Id_Player INT NOT NULL UNIQUE,
    Espaco_Maximo INT NOT NULL,
    Peso_Total INT NOT NULL,
    FOREIGN KEY (Id_Player) REFERENCES Personagem(id_Player)
);

-- Tabela Item
CREATE TABLE Item (
    id_item INT PRIMARY KEY,
    Peso INT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    preco INT
);

-- Tabela de Relacionamento entre Inventário e Item
CREATE TABLE Inventario_Item (
    Id_PlayerIn INT,
    id_item INT,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (Id_PlayerIn, id_item),
    FOREIGN KEY (Id_PlayerIn) REFERENCES Inventario(Id_PlayerIn) ON DELETE CASCADE,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),
    CHECK (quantidade > 0)
);