INSERT INTO Item (id_item, nome, Peso, tipo, preco) 
VALUES
(1, 'Sabre de Luz', 2, 'ARMA', 1000),
(2, 'Kit Médico', 1, 'CONSUMIVEL', 50),
(3, 'Armadura Clone', 8, 'ARMADURA', 500);
INSERT INTO Inventario (Id_PlayerIn, Id_Player, Espaco_Maximo, Peso_Total) 
VALUES 
(1, 1, 20, 11),
(2, 2, 15, 3);
INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade) 
VALUES
(1, 1, 1),
(1, 2, 2),
(1, 3, 1),
(2, 2, 3);