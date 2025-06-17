CREATE OR REPLACE FUNCTION equipar_jogador()
RETURNS TRIGGER AS $$
DECLARE
    novo_modelo_nave VARCHAR(30);
BEGIN
    -- cria inventario novo do jogador
    INSERT INTO Inventario (Id_PlayerIn, Id_Player, Espaco_Maximo, Peso_Total)
    VALUES (NEW.id_player, NEW.id_player, 20, 0);

    -- gera um modelo único para a nave YT-1300 do jogador
    novo_modelo_nave := 'YT-1300-' || LPAD(NEW.id_player::TEXT, 3, '0');

    -- cria uma nova nave YT-1300 para o jogador
    INSERT INTO Nave (modelo, Id_Player, velocidade, capacidade)
    VALUES (novo_modelo_nave, NEW.id_player, 145, 5);

    -- registra a nave na tabela específica YT_1300
    INSERT INTO YT_1300 (modelo)
    VALUES (novo_modelo_nave);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER novo_jogador_trigger
AFTER INSERT ON Personagem
FOR EACH ROW
EXECUTE FUNCTION equipar_jogador();