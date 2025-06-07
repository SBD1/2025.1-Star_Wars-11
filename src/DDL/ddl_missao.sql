CREATE TABLE Missao (
    id_missao INT PRIMARY KEY,
    valor_recompensa INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    nome_planeta VARCHAR(20) NOT NULL,
    id_NPC INT NOT NULL,
    level_minimo INT NOT NULL,
    FOREIGN KEY (nome_planeta) REFERENCES Planeta(nome_planeta),
    FOREIGN KEY (id_NPC) REFERENCES Npc(id_NPC)
);
