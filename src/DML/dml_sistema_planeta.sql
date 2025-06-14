INSERT INTO Sistema (id_sistema, nome_sistema) 
VALUES 
    (1, 'Sistema Tatooine'),
    (2, 'Sistema Coruscant'),
    (3, 'Sistema Naboo'),
    (4, 'Sistema Kashyyyk');

INSERT INTO Planeta (nome_planeta, habitavel, clima, id_sistema)
VALUES
    ('Tatooine', true, 'Desértico', 1),
    ('Coruscant', true, 'Temperado', 2),
    ('Naboo', true, 'Temperado', 3),
    ('Kashyyyk', true, 'Tropical', 4),
    ('Hoth', true, 'Gelado', 1);