CREATE TABLE Npc (
    id_NPC INT PRIMARY KEY,
    nome_planeta VARCHAR(20) NOT NULL,
    FOREIGN KEY (nome_planeta) REFERENCES Planeta(nome_planeta) # Assumindo Planeta table exists
);

CREATE TABLE Mercante (
    id_NPC INT NOT NULL,
    Itens_Disponiveis VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_NPC),
    FOREIGN KEY (id_NPC) REFERENCES Npc(id_NPC)
);

CREATE TABLE Mecanico (
    id_NPC INT NOT NULL,
    Servicos_disponiveis VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_NPC),
    FOREIGN KEY (id_NPC) REFERENCES Npc(id_NPC)
);
