CREATE OR REPLACE FUNCTION equipar_jogador()
RETURNS TRIGGER AS $$
BEGIN
    -- cria inventario novo do jogador
    INSERT INTO Inventario (Id_PlayerIn, Id_Player, Espaco_Maximo, Peso_Total) 
    VALUES (NEW.id_player, NEW.id_player, 20, 0);

    --todo jogador iniciará com a nave yt como base
    UPDATE Nave 
    SET Id_Player = NEW.id_player 
    WHERE modelo = 'YT-1300-001' 
    AND Id_Player IS NULL
    AND modelo IN (
        SELECT modelo 
        FROM Nave 
        WHERE modelo = 'YT-1300-001' 
        AND Id_Player IS NULL 
        LIMIT 1
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER novo_jogador_trigger
AFTER INSERT ON Personagem
FOR EACH ROW
EXECUTE FUNCTION equipar_jogador();