CREATE TABLE IF NOT EXISTS MOB (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    nivel_ameaca INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Inimigo (
    id_mob INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    vida_base INT NOT NULL DEFAULT 100,
    vida_atual INT NOT NULL DEFAULT 100,
    nivel INT NOT NULL DEFAULT 1,
    dano_base INT NOT NULL,
    pontos_escudo INT NOT NULL DEFAULT 0,
    creditos INT NOT NULL DEFAULT 0,
    tipo_mob VARCHAR(22) NOT NULL,
    planeta_origem VARCHAR(20) NOT NULL,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Normal (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Formacao_Tatica BOOLEAN NOT NULL DEFAULT false,
    Patrulha BOOLEAN NOT NULL DEFAULT false,
    Ataque_Coordenado BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Elite (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Armadura_Reforçada BOOLEAN NOT NULL DEFAULT false,
    Ataque_Especial BOOLEAN NOT NULL DEFAULT false,
    Regeneracao BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Boss (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Arsenal VARCHAR(20) NOT NULL,
    Habilidade_Unica BOOLEAN NOT NULL DEFAULT false,
    Invocacao_Aliados BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Inventario_IA (
    id_inventario INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_mob INT NOT NULL,
    item VARCHAR(50) NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    raridade VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob)
);

SELECT * FROM MOB;
SELECT * FROM Inimigo;
