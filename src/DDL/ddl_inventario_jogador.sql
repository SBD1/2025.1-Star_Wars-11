CREATE TABLE Inventario (
    Id_PlayerIn INT PRIMARY KEY,
    Id_Player INT NOT NULL UNIQUE,
    Espaco_Maximo INT NOT NULL DEFAULT 15,
    Peso_Total INT NOT NULL DEFAULT 0,
    FOREIGN KEY (Id_Player) REFERENCES Personagem(id_Player)
    ON DELETE CASCADE
);


CREATE TABLE Item (
    id_item INT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    Peso INT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    preco INT NOT NULL DEFAULT 0
);


CREATE TABLE Inventario_Item (
    Id_PlayerIn INT,
    id_item INT,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (Id_PlayerIn, id_item),
    FOREIGN KEY (Id_PlayerIn) REFERENCES Inventario(Id_PlayerIn) 
    ON DELETE CASCADE,
    FOREIGN KEY (id_item) REFERENCES Item(id_item),
    CHECK (quantidade > 0)
);