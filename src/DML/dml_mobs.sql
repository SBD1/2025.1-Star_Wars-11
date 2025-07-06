INSERT INTO MOB (tipo_mob, nivel_ameaca)
VALUES 
    ('Stormtrooper', 1),
    ('Dark Trooper', 2),
    ('Rancor', 3);

INSERT INTO Inimigo (vida_base, vida_atual, nivel, dano_base, pontos_escudo, creditos, tipo_mob, planeta_origem)
VALUES 
    (100, 100, 1, 20, 0, 50, 'Stormtrooper', 'Tatooine'),
    (200, 200, 5, 40, 50, 150, 'Dark Trooper', 'Coruscant'),
    (500, 500, 10, 100, 100, 500, 'Rancor', 'Tatooine');

INSERT INTO Normal (tipo_mob, Formacao_Tatica, Patrulha, Ataque_Coordenado)
VALUES ('Stormtrooper', true, true, true);

INSERT INTO Elite (tipo_mob, Armadura_Reforçada, Ataque_Especial, Regeneracao)
VALUES ('Dark Trooper', true, true, false);

INSERT INTO Boss (tipo_mob, Arsenal, Habilidade_Unica, Invocacao_Aliados)
VALUES ('Rancor', 'Garras e Presas', true, true);

INSERT INTO Inventario_IA (id_mob, item, quantidade, raridade)
VALUES 
    (1, 'Blaster E-11', 1, 'Comum'),
    (2, 'Dark Trooper Armor', 1, 'Raro'),
    (3, 'Garra do Rancor', 1, 'Épico');