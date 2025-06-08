CREATE TABLE IF NOT EXISTS Classe (
    nome_classe VARCHAR(22) PRIMARY KEY,
    Determinacao INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Personagem (
    id_player INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    vida_base INT NOT NULL DEFAULT 100,
    level INT NOT NULL DEFAULT 1,
    dano_base INT NOT NULL,
    xp INT NOT NULL DEFAULT 0,
    gcs INT NOT NULL DEFAULT 0,
    nome_classe VARCHAR(22) NOT NULL,
    nome_planeta VARCHAR(20) NOT NULL,
    FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe)
    --FOREIGN KEY (nome_planeta) REFERENCES Planeta(nome_planeta)
);

CREATE TABLE IF NOT EXISTS Jedi (
    nome_classe VARCHAR(22) PRIMARY KEY,
    Force_Heal BOOLEAN NOT NULL DEFAULT false,
    Force_Vision BOOLEAN NOT NULL DEFAULT false,
    Defensive_Force_Shield BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe)
);

CREATE TABLE IF NOT EXISTS Sith (
    nome_classe VARCHAR(22) PRIMARY KEY,
    Force_Corruption BOOLEAN NOT NULL DEFAULT false,
    Force_Lightning BOOLEAN NOT NULL DEFAULT false,
    Essence_Transfer BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe)
);

CREATE TABLE IF NOT EXISTS Cacador_de_Recompensas (
    nome_classe VARCHAR(22) PRIMARY KEY,
    Arsenal VARCHAR(20) NOT NULL,
    Master_Tracker BOOLEAN NOT NULL DEFAULT false,
    Clocking_Device BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe)
);

SELECT * FROM Classe;
SELECT * FROM Personagem 



