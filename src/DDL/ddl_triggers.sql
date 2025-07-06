CREATE OR REPLACE FUNCTION equipar_jogador()
RETURNS TRIGGER AS $$
DECLARE
    novo_modelo_nave VARCHAR(30);
    primeiro_setor_id INT;
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

    -- Colocar o jogador no primeiro setor do planeta escolhido
    SELECT s.id_setor INTO primeiro_setor_id
    FROM Setor s
    JOIN Cidade c ON s.id_cidade = c.id_cidade
    WHERE c.nome_planeta = NEW.nome_planeta
    ORDER BY s.nivel_perigo ASC, s.id_setor ASC
    LIMIT 1;

    -- Atualizar a localização do jogador
    IF primeiro_setor_id IS NOT NULL THEN
        UPDATE Personagem
        SET id_setor = primeiro_setor_id
        WHERE id_player = NEW.id_player;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER novo_jogador_trigger
AFTER INSERT ON Personagem
FOR EACH ROW
EXECUTE FUNCTION equipar_jogador();