CREATE TABLE Npc (
    id_NPC INT PRIMARY KEY,
    Nome_Planeta VARCHAR(50) NOT NULL,
    FOREIGN KEY (Nome_Planeta) REFERENCES Planeta(Nome_Planeta) # Assumindo Planeta table exists
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