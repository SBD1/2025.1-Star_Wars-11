CREATE TABLE Nave (
    modelo VARCHAR(30) PRIMARY KEY,
    Id_Player INT,
    velocidade INT NOT NULL,
    capacidade INT NOT NULL,
    FOREIGN KEY (Id_Player) REFERENCES Personagem(id_Player)
    ON DELETE SET NULL --nave n é perdida mesmo quando personagem some do banco de dados
);


CREATE TABLE X_WING_T65 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);


CREATE TABLE YT_1300 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);


CREATE TABLE Fregata_Corelliana_CR90 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);


CREATE TABLE Lambda_Class_Shuttle (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);