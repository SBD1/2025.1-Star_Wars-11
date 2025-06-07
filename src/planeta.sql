CREATE TABLE Planeta (
    nome_planeta VARCHAR(20) PRIMARY KEY,  -- mesmo tipo e tamanho
    habitavel BOOLEAN NOT NULL,
    clima TEXT,
    id_sistema INT NOT NULL,
    FOREIGN KEY (id_sistema) REFERENCES Sistema(id_sistema)
);
