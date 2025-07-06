-- =====================================================
-- SISTEMA DE LOCALIZAÇÃO HIERÁRQUICA
-- Planetas → Cidades → Setores (com Inimigos fixos)
-- =====================================================

-- Tabela de Cidades (cada planeta tem várias cidades)
CREATE TABLE IF NOT EXISTS Cidade (
    id_cidade INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    nome_cidade VARCHAR(50) NOT NULL,
    descricao TEXT,
    nome_planeta VARCHAR(20) NOT NULL,
    FOREIGN KEY (nome_planeta) REFERENCES Planeta(nome_planeta),
    UNIQUE(nome_cidade, nome_planeta)
);

-- Tabela de Setores (cada cidade tem vários setores)
CREATE TABLE IF NOT EXISTS Setor (
    id_setor INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    nome_setor VARCHAR(50) NOT NULL,
    descricao TEXT,
    tipo_setor VARCHAR(20) DEFAULT 'comum', -- comum, comercial, industrial, residencial, perigoso
    nivel_perigo INT DEFAULT 1, -- 1-5 (influencia inimigos)
    id_cidade INT NOT NULL,
    FOREIGN KEY (id_cidade) REFERENCES Cidade(id_cidade),
    UNIQUE(nome_setor, id_cidade)
);

-- Tabela de Inimigos por Setor (inimigos fixos em locais específicos)
CREATE TABLE IF NOT EXISTS Inimigo_Setor (
    id_inimigo_setor INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_mob INT NOT NULL,
    id_setor INT NOT NULL,
    quantidade_maxima INT DEFAULT 1, -- quantos deste inimigo podem existir no setor
    taxa_respawn INT DEFAULT 300, -- segundos para respawn
    ultimo_respawn TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true,
    FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob),
    FOREIGN KEY (id_setor) REFERENCES Setor(id_setor),
    UNIQUE(id_mob, id_setor)
);

-- Atualizar tabela Personagem para incluir localização específica
ALTER TABLE Personagem 
ADD COLUMN IF NOT EXISTS id_setor INT,
ADD CONSTRAINT fk_personagem_setor 
    FOREIGN KEY (id_setor) REFERENCES Setor(id_setor);

-- =====================================================
-- DADOS INICIAIS - CIDADES E SETORES
-- =====================================================

-- CORUSCANT - Capital Galáctica
INSERT INTO Cidade (nome_cidade, descricao, nome_planeta) VALUES
('Cidade Imperial', 'Centro político e administrativo da galáxia', 'Coruscant'),
('Distrito Comercial', 'Área de negócios e comércio intergaláctico', 'Coruscant'),
('Subníveis', 'Níveis inferiores da cidade, mais perigosos', 'Coruscant')
ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

-- Setores de Coruscant
INSERT INTO Setor (nome_setor, descricao, tipo_setor, nivel_perigo, id_cidade) VALUES
-- Cidade Imperial
('Palácio Imperial', 'Sede do poder galáctico', 'governamental', 1, 
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial' AND nome_planeta = 'Coruscant')),
('Senado Galáctico', 'Assembleia dos representantes planetários', 'governamental', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial' AND nome_planeta = 'Coruscant')),
('Quartel da Guarda', 'Base militar da capital', 'militar', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial' AND nome_planeta = 'Coruscant')),

-- Distrito Comercial  
('Centro de Negócios', 'Escritórios e corporações', 'comercial', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Comercial' AND nome_planeta = 'Coruscant')),
('Mercado Central', 'Grande mercado de bens diversos', 'comercial', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Comercial' AND nome_planeta = 'Coruscant')),
('Porto Espacial', 'Terminal de naves e cargas', 'comercial', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Comercial' AND nome_planeta = 'Coruscant')),

-- Subníveis
('Nível 1313', 'Área abandonada e perigosa', 'perigoso', 4,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Subníveis' AND nome_planeta = 'Coruscant')),
('Túneis de Manutenção', 'Sistema de túneis da cidade', 'industrial', 3,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Subníveis' AND nome_planeta = 'Coruscant'))
ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

-- TATOOINE - Planeta Desértico
INSERT INTO Cidade (nome_cidade, descricao, nome_planeta) VALUES
('Mos Eisley', 'Porto espacial famoso por sua cantina', 'Tatooine'),
('Mos Espa', 'Cidade de corridas de pods', 'Tatooine'),
('Deserto Jundland', 'Região selvagem e perigosa', 'Tatooine')
ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

-- Setores de Tatooine
INSERT INTO Setor (nome_setor, descricao, tipo_setor, nivel_perigo, id_cidade) VALUES
-- Mos Eisley
('Cantina de Chalmun', 'Bar famoso frequentado por contrabandistas', 'comercial', 3,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Eisley' AND nome_planeta = 'Tatooine')),
('Porto Espacial', 'Ancoradouro 94 e outras baias', 'comercial', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Eisley' AND nome_planeta = 'Tatooine')),
('Mercado de Sucata', 'Comércio de peças e equipamentos usados', 'comercial', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Eisley' AND nome_planeta = 'Tatooine')),

-- Mos Espa
('Arena de Corridas', 'Pista de corrida de pods', 'esportivo', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Espa' AND nome_planeta = 'Tatooine')),
('Bairro dos Escravos', 'Área residencial dos trabalhadores', 'residencial', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Espa' AND nome_planeta = 'Tatooine')),

-- Deserto Jundland
('Desfiladeiro Rochoso', 'Formações rochosas perigosas', 'perigoso', 4,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Deserto Jundland' AND nome_planeta = 'Tatooine')),
('Oasis Perdido', 'Rara fonte de água no deserto', 'natural', 3,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Deserto Jundland' AND nome_planeta = 'Tatooine'))
ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

-- NABOO - Planeta Pacífico
INSERT INTO Cidade (nome_cidade, descricao, nome_planeta) VALUES
('Theed', 'Capital elegante de Naboo', 'Naboo'),
('Otoh Gunga', 'Cidade submarina dos Gungans', 'Naboo'),
('Planícies Verdes', 'Campos abertos e florestas', 'Naboo')
ON CONFLICT (nome_cidade, nome_planeta) DO NOTHING;

-- Setores de Naboo
INSERT INTO Setor (nome_setor, descricao, tipo_setor, nivel_perigo, id_cidade) VALUES
-- Theed
('Palácio Real', 'Residência da Rainha de Naboo', 'governamental', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed' AND nome_planeta = 'Naboo')),
('Jardins Reais', 'Belos jardins do palácio', 'natural', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed' AND nome_planeta = 'Naboo')),
('Plaza Central', 'Praça principal da cidade', 'comercial', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed' AND nome_planeta = 'Naboo')),

-- Otoh Gunga
('Câmara do Conselho', 'Centro de governo Gungan', 'governamental', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Otoh Gunga' AND nome_planeta = 'Naboo')),
('Distrito Residencial', 'Casas-bolha dos Gungans', 'residencial', 1,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Otoh Gunga' AND nome_planeta = 'Naboo')),

-- Planícies Verdes
('Floresta Sagrada', 'Antiga floresta com criaturas selvagens', 'natural', 2,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Planícies Verdes' AND nome_planeta = 'Naboo')),
('Campo de Batalha', 'Local de antigas batalhas', 'histórico', 3,
    (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Planícies Verdes' AND nome_planeta = 'Naboo'))
ON CONFLICT (nome_setor, id_cidade) DO NOTHING;

-- =====================================================
-- DISTRIBUIÇÃO DE INIMIGOS NOS SETORES
-- =====================================================

-- CORUSCANT - Inimigos por setor
-- Quartel da Guarda (nível perigo 2)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 2, 180
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Coruscant'
AND i.tipo_mob = 'Stormtrooper'
AND s.nome_setor = 'Quartel da Guarda'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Coruscant'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- Nível 1313 (nível perigo 4) - Inimigos mais perigosos
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 1, 300
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Coruscant'
AND i.tipo_mob IN ('Sith_Warrior', 'Dark_Trooper')
AND s.nome_setor = 'Nível 1313'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Coruscant'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- Túneis de Manutenção (nível perigo 3)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 3, 240
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Coruscant'
AND i.tipo_mob = 'Smuggler'
AND s.nome_setor = 'Túneis de Manutenção'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Coruscant'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- TATOOINE - Inimigos por setor
-- Cantina de Chalmun (nível perigo 3)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 2, 200
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Tatooine'
AND i.tipo_mob IN ('Smuggler', 'Bounty_Hunter')
AND s.nome_setor = 'Cantina de Chalmun'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Tatooine'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- Desfiladeiro Rochoso (nível perigo 4)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 1, 360
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Tatooine'
AND i.tipo_mob = 'Tusken_Raider'
AND s.nome_setor = 'Desfiladeiro Rochoso'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Tatooine'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- Mercado de Sucata (nível perigo 2)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 2, 150
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Tatooine'
AND i.tipo_mob = 'Jawa'
AND s.nome_setor = 'Mercado de Sucata'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Tatooine'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- NABOO - Inimigos por setor (planeta mais pacífico)
-- Floresta Sagrada (nível perigo 2)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 3, 120
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Naboo'
AND i.tipo_mob = 'Battle_Droid'
AND s.nome_setor = 'Floresta Sagrada'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Naboo'
ON CONFLICT (id_mob, id_setor) DO NOTHING;

-- Campo de Batalha (nível perigo 3)
INSERT INTO Inimigo_Setor (id_mob, id_setor, quantidade_maxima, taxa_respawn)
SELECT i.id_mob, s.id_setor, 2, 180
FROM Inimigo i, Setor s, Cidade c
WHERE i.planeta_origem = 'Naboo'
AND i.tipo_mob IN ('Battle_Droid', 'Droideka')
AND s.nome_setor = 'Campo de Batalha'
AND s.id_cidade = c.id_cidade
AND c.nome_planeta = 'Naboo'
ON CONFLICT (id_mob, id_setor) DO NOTHING;
