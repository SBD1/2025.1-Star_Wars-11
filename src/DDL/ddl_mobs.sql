CREATE TABLE IF NOT EXISTS MOB (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    nivel_ameaca INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Inimigo (
    id_mob INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    vida_base INT NOT NULL DEFAULT 100,
    nivel INT NOT NULL DEFAULT 1,
    dano_base INT NOT NULL,
    pontos_escudo INT NOT NULL DEFAULT 0,
    creditos INT NOT NULL DEFAULT 0,
    tipo_mob VARCHAR(22) NOT NULL,
    planeta_origem VARCHAR(20) NOT NULL,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Normal (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Formacao_Tatica BOOLEAN NOT NULL DEFAULT false,
    Patrulha BOOLEAN NOT NULL DEFAULT false,
    Ataque_Coordenado BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Elite (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Armadura_Reforçada BOOLEAN NOT NULL DEFAULT false,
    Ataque_Especial BOOLEAN NOT NULL DEFAULT false,
    Regeneracao BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Boss (
    tipo_mob VARCHAR(22) PRIMARY KEY,
    Arsenal VARCHAR(20) NOT NULL,
    Habilidade_Unica BOOLEAN NOT NULL DEFAULT false,
    Invocacao_Aliados BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (tipo_mob) REFERENCES MOB(tipo_mob)
);

CREATE TABLE IF NOT EXISTS Inventario_IA (
    id_inventario INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_mob INT NOT NULL,
    item VARCHAR(50) NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    raridade VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob)
);

-- =================================================================
-- SCRIPT PARA MIGRAR E PRESERVAR DADOS DO Inventario_IA
-- Converte a coluna de texto 'item' para 'id_item' sem perder dados.
-- =================================================================

-- PASSO 1: Garantir que as colunas de destino existam.
-- É seguro rodar, pois o IF NOT EXISTS previne erros.
ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS id_item INT;
ALTER TABLE Inventario_IA ADD COLUMN IF NOT EXISTS drop_rarity VARCHAR(20);


-- PASSO 2: Inserir na tabela 'Item' todos os itens que existem no
-- inventário dos inimigos mas não na tabela de itens principal.
-- Usamos um CTE (WITH) para encontrar os nomes únicos primeiro.
WITH unique_items_from_ia AS (
    SELECT DISTINCT item AS nome_item FROM Inventario_IA WHERE item IS NOT NULL
)
INSERT INTO Item (id_item, nome, Peso, tipo, preco, efeito_tipo, efeito_valor)
SELECT
    -- Gera um ID alto para não conflitar com os IDs que já criou.
    -- (row_number() over ()) gera uma sequência: 1, 2, 3...
    -- 1000 + (row_number() over ()) resulta em: 1001, 1002, 1003...
    1000 + (row_number() over ()), 
    ui.nome_item,
    1, -- Peso padrão
    'Recurso', -- Tipo padrão
    10, -- Preço padrão
    NULL, -- Sem efeito
    NULL  -- Sem valor de efeito
FROM unique_items_from_ia ui
-- A cláusula LEFT JOIN ... IS NULL garante que só inserimos itens que NÃO existem na tabela Item.
LEFT JOIN Item i ON ui.nome_item = i.nome
WHERE i.id_item IS NULL;


-- PASSO 3: Atualizar a coluna 'id_item' na tabela Inventario_IA.
-- Para cada linha em Inventario_IA, buscamos o ID correspondente na tabela Item.
UPDATE Inventario_IA ia
SET id_item = i.id_item
FROM Item i
WHERE ia.item = i.nome;

-- PASSO 4: Copiar os dados da coluna 'raridade' para a nova 'drop_rarity'
UPDATE Inventario_IA
SET drop_rarity = raridade
WHERE raridade IS NOT NULL;

ALTER TABLE Inventario_IA ALTER COLUMN id_item SET NOT NULL;


-- , removendo as colunas antigas que não são mais necessárias.
ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS item;
ALTER TABLE Inventario_IA DROP COLUMN IF EXISTS raridade;

--  Adicionar a chave estrangeira para garantir a integridade.
ALTER TABLE Inventario_IA DROP CONSTRAINT IF EXISTS inventario_ia_id_item_fkey;
ALTER TABLE Inventario_IA ADD CONSTRAINT inventario_ia_id_item_fkey
    FOREIGN KEY (id_item) REFERENCES Item(id_item) ON DELETE CASCADE;

