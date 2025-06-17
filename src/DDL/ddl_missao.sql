DROP TABLE IF EXISTS Missao_Jogador CASCADE;
DROP TABLE IF EXISTS Missao CASCADE;

CREATE TABLE Missao (
    id_missao INT PRIMARY KEY,
    nome_missao VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    valor_recompensa INT NOT NULL,
    xp_recompensa INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'Disponível',
    nome_planeta VARCHAR(20) NOT NULL,
    id_NPC INT NOT NULL,
    level_minimo INT NOT NULL,
    tipo_missao VARCHAR(20) NOT NULL DEFAULT 'Entrega'
);

--Rastreia missoes do jogador
CREATE TABLE Missao_Jogador (
    id_player INT NOT NULL,
    id_missao INT NOT NULL,
    status_jogador VARCHAR(20) NOT NULL DEFAULT 'Em Andamento',
    data_aceita TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_player, id_missao)
);
