CREATE TABLE IF NOT EXISTS Personagem (
    id_player INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1) NOT NULL PRIMARY KEY,
    vida_base INTEGER NOT NULL DEFAULT 100,
    level INTEGER NOT NULL DEFAULT 1,
    dano_base INTEGER NOT NULL,
    xp INTEGER NOT NULL DEFAULT 0,
    gcs INTEGER NOT NULL DEFAULT 0,
    nome_classe VARCHAR(20) NOT NULL,
    nome_planeta VARCHAR(20) NOT NULL

    -- CONSTRAINT fk_classe FOREIGN KEY (nome_classe) REFERENCES Classe(nome_classe),
    -- CONSTRAINT fk_planeta FOREIGN KEY (nome_planeta) REFERENCES Planeta(nome_planeta)
)