-- Adicionar inimigos especificos para os novos setores

-- Inimigos para setores perigosos de Tatooine
INSERT INTO Inimigo_Setor (id_inimigo, id_setor, quantidade_maxima, tempo_respawn_minutos) VALUES
-- Periferia do Deserto (Anchorhead) - Tusken Raiders
(2, (SELECT id_setor FROM Setor WHERE nome_setor = 'Periferia do Deserto'), 2, 15),
-- Quartel Imperial (Bestine) - Stormtroopers
(1, (SELECT id_setor FROM Setor WHERE nome_setor = 'Quartel Imperial'), 3, 10),
-- Pista de Corrida (Mos Espa Arena) - Sebulba (se existir) ou Stormtroopers
(1, (SELECT id_setor FROM Setor WHERE nome_setor = 'Pista de Corrida'), 2, 12);

-- Inimigos para Coruscant
INSERT INTO Inimigo_Setor (id_inimigo, id_setor, quantidade_maxima, tempo_respawn_minutos) VALUES
-- Templo Jedi Abandonado - Inimigos mais fortes
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Templo Jedi Abandonado'), 1, 30),
-- Nivel 1313 - Inimigos muito perigosos
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Nivel 1313'), 2, 20),
-- Mercado Negro - Contrabandistas
(1, (SELECT id_setor FROM Setor WHERE nome_setor = 'Mercado Negro'), 2, 15),
-- Refugio de Contrabandistas - Criminosos
(2, (SELECT id_setor FROM Setor WHERE nome_setor = 'Refugio de Contrabandistas'), 3, 12);

-- Inimigos para Naboo
INSERT INTO Inimigo_Setor (id_inimigo, id_setor, quantidade_maxima, tempo_respawn_minutos) VALUES
-- Lago Profundo - Criaturas aquaticas
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Lago Profundo'), 1, 25);

-- Inimigos para Kashyyyk
INSERT INTO Inimigo_Setor (id_inimigo, id_setor, quantidade_maxima, tempo_respawn_minutos) VALUES
-- Posto Avancado - Tropas imperiais
(1, (SELECT id_setor FROM Setor WHERE nome_setor = 'Posto Avancado'), 2, 10),
-- Raizes Profundas - Criaturas da floresta
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Raizes Profundas'), 2, 18),
-- Cavernas Ocultas - Criaturas perigosas
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Cavernas Ocultas'), 1, 22);

-- Inimigos para Hoth
INSERT INTO Inimigo_Setor (id_inimigo, id_setor, quantidade_maxima, tempo_respawn_minutos) VALUES
-- Campo de Gelo Norte - Wampas (usando Rancor como placeholder)
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Campo de Gelo Norte'), 1, 30),
-- Destrocos de Nave - Droides imperiais
(1, (SELECT id_setor FROM Setor WHERE nome_setor = 'Destrocos de Nave'), 2, 15),
-- Camara Profunda - Criaturas do gelo
(3, (SELECT id_setor FROM Setor WHERE nome_setor = 'Camara Profunda'), 1, 25);
