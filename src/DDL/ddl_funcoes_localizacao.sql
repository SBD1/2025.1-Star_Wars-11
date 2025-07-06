-- =====================================================
-- FUNCOES PARA SISTEMA DE LOCALIZACAO HIERARQUICA
-- =====================================================

-- Funcao para listar cidades de um planeta
CREATE OR REPLACE FUNCTION listar_cidades_planeta(planeta_nome VARCHAR(20))
RETURNS TABLE(
    id_cidade INT,
    nome_cidade VARCHAR(50),
    descricao TEXT,
    total_setores BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id_cidade,
        c.nome_cidade,
        c.descricao,
        COUNT(s.id_setor) as total_setores
    FROM Cidade c
    LEFT JOIN Setor s ON c.id_cidade = s.id_cidade
    WHERE c.nome_planeta = planeta_nome
    GROUP BY c.id_cidade, c.nome_cidade, c.descricao
    ORDER BY c.nome_cidade;
END;
$$ LANGUAGE plpgsql;

-- Funcao para listar setores de uma cidade
CREATE OR REPLACE FUNCTION listar_setores_cidade(cidade_id INT)
RETURNS TABLE(
    id_setor INT,
    nome_setor VARCHAR(50),
    descricao TEXT,
    tipo_setor VARCHAR(20),
    nivel_perigo INT,
    total_inimigos BIGINT,
    inimigos_ativos BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        s.id_setor,
        s.nome_setor,
        s.descricao,
        s.tipo_setor,
        s.nivel_perigo,
        COUNT(ins.id_inimigo_setor) as total_inimigos,
        COUNT(CASE WHEN ins.ativo = true THEN 1 END) as inimigos_ativos
    FROM Setor s
    LEFT JOIN Inimigo_Setor ins ON s.id_setor = ins.id_setor
    WHERE s.id_cidade = cidade_id
    GROUP BY s.id_setor, s.nome_setor, s.descricao, s.tipo_setor, s.nivel_perigo
    ORDER BY s.nivel_perigo, s.nome_setor;
END;
$$ LANGUAGE plpgsql;

-- Funcao para obter localizacao atual do jogador
CREATE OR REPLACE FUNCTION obter_localizacao_jogador(jogador_id INT)
RETURNS TABLE(
    planeta VARCHAR(20),
    cidade VARCHAR(50),
    setor VARCHAR(50),
    id_setor_atual INT,
    tipo_setor VARCHAR(20),
    nivel_perigo INT,
    descricao_setor TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        pl.nome_planeta,
        c.nome_cidade,
        s.nome_setor,
        s.id_setor,
        s.tipo_setor,
        s.nivel_perigo,
        s.descricao
    FROM Personagem p
    LEFT JOIN Setor s ON p.id_setor = s.id_setor
    LEFT JOIN Cidade c ON s.id_cidade = c.id_cidade
    LEFT JOIN Planeta pl ON c.nome_planeta = pl.nome_planeta
    WHERE p.id_player = jogador_id;
END;
$$ LANGUAGE plpgsql;

-- Funcao para mover jogador para um setor especifico
CREATE OR REPLACE FUNCTION mover_jogador_setor(jogador_id INT, novo_setor_id INT)
RETURNS TEXT AS $$
DECLARE
    setor_existe BOOLEAN := FALSE;
    nome_setor VARCHAR(50);
    nome_cidade VARCHAR(50);
    planeta_setor VARCHAR(20);
    planeta_jogador VARCHAR(20);
BEGIN
    -- Verificar se o setor existe
    SELECT s.nome_setor, c.nome_cidade, c.nome_planeta INTO nome_setor, nome_cidade, planeta_setor
    FROM Setor s
    JOIN Cidade c ON s.id_cidade = c.id_cidade
    WHERE s.id_setor = novo_setor_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Setor nao encontrado';
    END IF;
    
    -- Verificar se o jogador esta no mesmo planeta
    SELECT nome_planeta INTO planeta_jogador
    FROM Personagem WHERE id_player = jogador_id;
    
    IF planeta_jogador != planeta_setor THEN
        RETURN 'Erro: Voce nao pode se mover para um setor em outro planeta';
    END IF;
    
    -- Mover jogador
    UPDATE Personagem
    SET id_setor = novo_setor_id
    WHERE id_player = jogador_id;
    
    RETURN 'Voce se moveu para: ' || nome_setor || ' (' || nome_cidade || ')';
END;
$$ LANGUAGE plpgsql;

-- Funcao para listar cidades disponiveis para o jogador (sem custo)
CREATE OR REPLACE FUNCTION listar_cidades_disponiveis(jogador_id INT)
RETURNS TABLE(
    id_cidade INT,
    nome_cidade VARCHAR(50),
    nome_planeta VARCHAR(20),
    descricao TEXT,
    total_setores BIGINT
) AS $$
DECLARE
    planeta_atual VARCHAR(20);
BEGIN
    -- Obter planeta atual do jogador
    SELECT nome_planeta INTO planeta_atual
    FROM Personagem WHERE id_player = jogador_id;
    
    RETURN QUERY
    SELECT 
        c.id_cidade,
        c.nome_cidade,
        c.nome_planeta,
        c.descricao,
        COUNT(s.id_setor) as total_setores
    FROM Cidade c
    LEFT JOIN Setor s ON c.id_cidade = s.id_cidade
    WHERE c.nome_planeta = planeta_atual
    GROUP BY c.id_cidade, c.nome_cidade, c.nome_planeta, c.descricao
    ORDER BY c.nome_cidade;
END;
$$ LANGUAGE plpgsql;

-- Funcao para viajar para uma cidade (sem custo)
CREATE OR REPLACE FUNCTION viajar_para_cidade(jogador_id INT, cidade_id INT)
RETURNS TEXT AS $$
DECLARE
    nome_cidade VARCHAR(50);
    planeta_cidade VARCHAR(20);
    planeta_jogador VARCHAR(20);
    primeiro_setor_id INT;
    nome_primeiro_setor VARCHAR(50);
BEGIN
    -- Verificar se a cidade existe
    SELECT c.nome_cidade, c.nome_planeta INTO nome_cidade, planeta_cidade
    FROM Cidade c WHERE c.id_cidade = cidade_id;
    
    IF NOT FOUND THEN
        RETURN 'Erro: Cidade nao encontrada';
    END IF;
    
    -- Verificar se o jogador esta no mesmo planeta
    SELECT nome_planeta INTO planeta_jogador
    FROM Personagem WHERE id_player = jogador_id;
    
    IF planeta_jogador != planeta_cidade THEN
        RETURN 'Erro: Voce nao pode viajar para uma cidade em outro planeta';
    END IF;
    
    -- Encontrar o primeiro setor da cidade
    SELECT id_setor, nome_setor INTO primeiro_setor_id, nome_primeiro_setor
    FROM Setor 
    WHERE id_cidade = cidade_id 
    ORDER BY id_setor 
    LIMIT 1;
    
    IF primeiro_setor_id IS NULL THEN
        RETURN 'Erro: Esta cidade nao possui setores disponiveis';
    END IF;
    
    -- Mover jogador para o primeiro setor da cidade
    UPDATE Personagem
    SET id_setor = primeiro_setor_id
    WHERE id_player = jogador_id;
    
    RETURN 'Voce viajou para ' || nome_cidade || ' e chegou em: ' || nome_primeiro_setor;
END;
$$ LANGUAGE plpgsql;

-- Funcao para listar planetas disponiveis para viagem
CREATE OR REPLACE FUNCTION listar_planetas_disponiveis(jogador_id INT)
RETURNS TABLE(
    nome_planeta VARCHAR(20),
    clima VARCHAR(20),
    populacao BIGINT,
    afiliacao VARCHAR(20),
    total_cidades BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.nome_planeta,
        p.clima,
        p.populacao,
        p.afiliacao,
        COUNT(c.id_cidade) as total_cidades
    FROM Planeta p
    LEFT JOIN Cidade c ON p.nome_planeta = c.nome_planeta
    GROUP BY p.nome_planeta, p.clima, p.populacao, p.afiliacao
    ORDER BY p.nome_planeta;
END;
$$ LANGUAGE plpgsql;

-- Funcao para viajar entre planetas (requer nave)
CREATE OR REPLACE FUNCTION viajar_para_planeta(jogador_id INT, planeta_destino VARCHAR(20))
RETURNS TEXT AS $$
DECLARE
    nave_jogador VARCHAR(20);
    velocidade_nave INT;
    planeta_atual VARCHAR(20);
    primeira_cidade_id INT;
    nome_primeira_cidade VARCHAR(50);
    primeiro_setor_id INT;
    nome_primeiro_setor VARCHAR(50);
BEGIN
    -- Verificar se o planeta existe
    IF NOT EXISTS (SELECT 1 FROM Planeta WHERE nome_planeta = planeta_destino) THEN
        RETURN 'Erro: Planeta nao encontrado';
    END IF;
    
    -- Obter dados do jogador
    SELECT nome_planeta, nome_nave INTO planeta_atual, nave_jogador
    FROM Personagem WHERE id_player = jogador_id;
    
    IF planeta_atual = planeta_destino THEN
        RETURN 'Erro: Voce ja esta neste planeta';
    END IF;
    
    -- Verificar se tem nave
    IF nave_jogador IS NULL THEN
        RETURN 'Erro: Voce precisa de uma nave para viajar entre planetas';
    END IF;
    
    -- Verificar velocidade da nave
    SELECT velocidade INTO velocidade_nave
    FROM Nave WHERE nome_nave = nave_jogador;
    
    -- Encontrar primeira cidade do planeta destino
    SELECT id_cidade, nome_cidade INTO primeira_cidade_id, nome_primeira_cidade
    FROM Cidade 
    WHERE nome_planeta = planeta_destino 
    ORDER BY id_cidade 
    LIMIT 1;
    
    IF primeira_cidade_id IS NULL THEN
        RETURN 'Erro: Este planeta nao possui cidades disponiveis';
    END IF;
    
    -- Encontrar primeiro setor da primeira cidade
    SELECT id_setor, nome_setor INTO primeiro_setor_id, nome_primeiro_setor
    FROM Setor 
    WHERE id_cidade = primeira_cidade_id 
    ORDER BY id_setor 
    LIMIT 1;
    
    -- Mover jogador
    UPDATE Personagem
    SET nome_planeta = planeta_destino,
        id_setor = primeiro_setor_id
    WHERE id_player = jogador_id;
    
    RETURN 'Voce viajou para ' || planeta_destino || ' e chegou em: ' || nome_primeira_cidade || ' - ' || nome_primeiro_setor;
END;
$$ LANGUAGE plpgsql;

-- Funcao para listar inimigos do setor atual do jogador
CREATE OR REPLACE FUNCTION listar_inimigos_setor_jogador(jogador_id INT)
RETURNS TABLE (
    id_mob INT,
    tipo_mob VARCHAR(22),
    vida_base INT,
    nivel INT,
    dano_base INT,
    pontos_escudo INT,
    creditos INT,
    nivel_ameaca INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        i.id_mob,
        i.tipo_mob,
        i.vida_base,
        i.nivel,
        i.dano_base,
        i.pontos_escudo,
        i.creditos,
        m.nivel_ameaca
    FROM Inimigo i
    JOIN MOB m ON i.tipo_mob = m.tipo_mob
    JOIN Inimigo_Setor ins ON i.id_mob = ins.id_mob
    JOIN Personagem p ON p.id_setor = ins.id_setor
    WHERE p.id_player = jogador_id
    ORDER BY m.nivel_ameaca, i.nivel;
END;
$$ LANGUAGE plpgsql;
