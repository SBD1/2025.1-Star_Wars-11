-- Expansao de cidades e setores para todos os planetas

-- TATOOINE - Adicionar mais setores para cidades existentes e novas cidades
INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
('Anchorhead', 'Tatooine', 'Pequena cidade de mineracao no deserto'),
('Bestine', 'Tatooine', 'Capital administrativa de Tatooine'),
('Mos Espa Arena', 'Tatooine', 'Arena de corridas de pods famosa');

-- Setores para Anchorhead
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Centro de Mineracao', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Anchorhead'), 'industrial', 2, 'Operacoes de mineracao de umidade'),
('Mercado Local', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Anchorhead'), 'comercial', 1, 'Pequeno mercado para suprimentos'),
('Periferia do Deserto', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Anchorhead'), 'perigoso', 4, 'Limite da cidade com o deserto selvagem');

-- Setores para Bestine
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Palacio do Governador', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Bestine'), 'administrativo', 1, 'Sede do governo planetario'),
('Quartel Imperial', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Bestine'), 'militar', 3, 'Base das tropas imperiais'),
('Distrito Comercial', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Bestine'), 'comercial', 2, 'Area comercial principal da capital');

-- Setores para Mos Espa Arena
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Pista de Corrida', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Espa Arena'), 'esportivo', 3, 'Circuito principal das corridas de pods'),
('Boxes dos Pilotos', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Mos Espa Arena'), 'comercial', 2, 'Area de preparacao dos pods');

-- CORUSCANT - Adicionar cidades e setores
INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
('Cidade Imperial', 'Coruscant', 'Centro do poder imperial na galaxia'),
('Subniveis', 'Coruscant', 'Niveis inferiores da cidade-planeta'),
('Distrito Senatorial', 'Coruscant', 'Area residencial dos senadores');

-- Setores para Cidade Imperial
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Palacio Imperial', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial'), 'administrativo', 1, 'Residencia do Imperador'),
('Academia Imperial', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial'), 'militar', 2, 'Treinamento de oficiais imperiais'),
('Praca Central', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial'), 'comercial', 1, 'Centro comercial da capital'),
('Templo Jedi Abandonado', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cidade Imperial'), 'historico', 3, 'Ruinas do antigo templo Jedi');

-- Setores para Subniveis
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Nivel 1313', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Subniveis'), 'perigoso', 5, 'Nivel mais perigoso dos subniveis'),
('Mercado Negro', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Subniveis'), 'comercial', 4, 'Comercio ilegal nos subniveis'),
('Refugio de Contrabandistas', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Subniveis'), 'perigoso', 4, 'Esconderijo de criminosos');

-- Setores para Distrito Senatorial
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Residencias Senatoriais', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Senatorial'), 'residencial', 1, 'Casas dos senadores'),
('Senado Galactico', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Senatorial'), 'administrativo', 1, 'Edificio do senado'),
('Jardins da Republica', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Distrito Senatorial'), 'pacifico', 1, 'Jardins ornamentais');

-- NABOO - Adicionar cidades e setores
INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
('Theed', 'Naboo', 'Capital real de Naboo'),
('Otoh Gunga', 'Naboo', 'Cidade submarina dos Gungans'),
('Keren', 'Naboo', 'Cidade montanhosa de Naboo');

-- Setores para Theed
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Palacio Real', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed'), 'administrativo', 1, 'Residencia da Rainha de Naboo'),
('Hangar Real', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed'), 'militar', 2, 'Hangar das naves reais'),
('Praca da Liberdade', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed'), 'pacifico', 1, 'Praca central da cidade'),
('Geradores de Energia', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Theed'), 'industrial', 2, 'Complexo energetico da cidade');

-- Setores para Otoh Gunga
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Camara do Conselho', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Otoh Gunga'), 'administrativo', 1, 'Centro de governo Gungan'),
('Bolhas Residenciais', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Otoh Gunga'), 'residencial', 1, 'Casas dos Gungans'),
('Lago Profundo', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Otoh Gunga'), 'aquatico', 3, 'Aguas profundas com criaturas');

-- Setores para Keren
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Observatorio', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Keren'), 'cientifico', 1, 'Centro de observacao astronomica'),
('Trilhas Montanhosas', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Keren'), 'natural', 2, 'Caminhos nas montanhas');

-- KASHYYYK - Adicionar cidades e setores
INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
('Rwookrrorro', 'Kashyyyk', 'Cidade principal dos Wookiees nas arvores'),
('Kachirho', 'Kashyyyk', 'Cidade costeira dos Wookiees'),
('Floresta Sombria', 'Kashyyyk', 'Regiao perigosa da floresta');

-- Setores para Rwookrrorro
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Copas das Arvores', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Rwookrrorro'), 'residencial', 1, 'Casas Wookiee nas arvores'),
('Plataforma de Pouso', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Rwookrrorro'), 'comercial', 2, 'Area de chegada de naves'),
('Conselho dos Ancioes', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Rwookrrorro'), 'administrativo', 1, 'Centro de decisoes Wookiee');

-- Setores para Kachirho
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Praia Wookiee', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Kachirho'), 'natural', 2, 'Costa do oceano de Kashyyyk'),
('Estaleiro', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Kachirho'), 'industrial', 2, 'Construcao de embarcacoes'),
('Posto Avancado', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Kachirho'), 'militar', 3, 'Base de defesa costeira');

-- Setores para Floresta Sombria
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Raizes Profundas', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Floresta Sombria'), 'perigoso', 5, 'Nivel do solo da floresta'),
('Cavernas Ocultas', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Floresta Sombria'), 'perigoso', 4, 'Cavernas com criaturas perigosas');

-- HOTH - Adicionar cidades e setores
INSERT INTO Cidade (nome_cidade, nome_planeta, descricao) VALUES
('Base Echo', 'Hoth', 'Base rebelde abandonada no gelo'),
('Planicie Gelada', 'Hoth', 'Vasta extensao de gelo e neve'),
('Cavernas de Gelo', 'Hoth', 'Sistema de cavernas congeladas');

-- Setores para Base Echo
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Hangar Principal', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Base Echo'), 'militar', 2, 'Hangar da antiga base rebelde'),
('Centro de Comando', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Base Echo'), 'militar', 2, 'Sala de operacoes abandonada'),
('Geradores de Energia', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Base Echo'), 'industrial', 3, 'Geradores danificados');

-- Setores para Planicie Gelada
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Campo de Gelo Norte', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Planicie Gelada'), 'natural', 4, 'Planicie gelada com tempestades'),
('Destrocos de Nave', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Planicie Gelada'), 'perigoso', 3, 'Restos de naves acidentadas');

-- Setores para Cavernas de Gelo
INSERT INTO Setor (nome_setor, id_cidade, tipo_setor, nivel_perigo, descricao) VALUES
('Tunel Principal', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cavernas de Gelo'), 'natural', 3, 'Passagem principal das cavernas'),
('Camara Profunda', (SELECT id_cidade FROM Cidade WHERE nome_cidade = 'Cavernas de Gelo'), 'perigoso', 4, 'Camara mais profunda com criaturas');
