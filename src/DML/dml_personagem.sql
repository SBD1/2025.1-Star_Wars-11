INSERT INTO Classe (nome_classe, Determinacao) 
VALUES 
    ('Jedi', 10),
    ('Sith', 8),
    ('Cacador_de_Recompensas', 7);

INSERT INTO Personagem (id_player, vida_base, level, dano_base, xp, gcs, nome_classe, nome_planeta) 
OVERRIDING SYSTEM VALUE
VALUES 
    (1, 100, 1, 10, 0, 1000, 'Jedi', 'Tatooine'),
    (2, 100, 1, 10, 0, 1000, 'Sith', 'Coruscant'),
    (3, 100, 1, 10, 0, 1000, 'Cacador_de_Recompensas', 'Naboo');