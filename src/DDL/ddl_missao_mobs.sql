CREATE TABLE Missao_Mobs (
   id_mob INT NOT NULL,
   id_missao INT NOT NULL,
   tipo_mob VARCHAR(22) NOT NULL,
   planeta_origem VARCHAR(20) NOT NULL,
   setor VARCHAR(20) NOT NULL,
   xp_recompensa INT NOT NULL DEFAULT 0,
   creditos_recompensa INT NOT NULL DEFAULT 0,
   nivel_minimo INT NOT NULL DEFAULT 1,
   ativa BOOLEAN NOT NULL DEFAULT true,
   FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob),
   FOREIGN KEY (id_missao) REFERENCES Missao(id_missao)

);