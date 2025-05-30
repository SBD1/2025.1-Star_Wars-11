-- Criação das tabelas relacionadas a Naves

-- Tabela Nave (Genérica)
CREATE TABLE Nave (
    modelo VARCHAR(30) PRIMARY KEY,
    Id_Player INT,
    velocidade INT NOT NULL,
    capacidade INT NOT NULL,
    FOREIGN KEY (Id_Player) REFERENCES Personagem(id_Player)
);

-- Tabela X WING T-65 (Especialização de Nave)
CREATE TABLE X_WING_T65 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);

-- Tabela YT-1300 (Especialização de Nave)
CREATE TABLE YT_1300 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);

-- Tabela Fregata Corelliana CR90 (Especialização de Nave)
CREATE TABLE Fregata_Corelliana_CR90 (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);

-- Tabela Lambda-class Shuttle (Especialização de Nave)
CREATE TABLE Lambda_Class_Shuttle (
    modelo VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (modelo) REFERENCES Nave(modelo) ON DELETE CASCADE
);
