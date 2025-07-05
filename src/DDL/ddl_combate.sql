-- =====================================================
-- DDL Sistema de Combate - Star Wars MUD
-- =====================================================

-- Tabela principal para registrar combates ativos
CREATE TABLE IF NOT EXISTS Combate (
    id_combate INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_player INT NOT NULL,
    id_mob INT NOT NULL,
    vida_jogador_atual INT NOT NULL,
    vida_inimigo_atual INT NOT NULL,
    turno_atual VARCHAR(10) NOT NULL DEFAULT 'jogador', -- 'jogador' ou 'inimigo'
    status_combate VARCHAR(20) NOT NULL DEFAULT 'ativo', -- 'ativo', 'finalizado', 'fugiu'
    data_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_fim TIMESTAMP NULL,
    FOREIGN KEY (id_player) REFERENCES Personagem(id_player) ON DELETE CASCADE,
    FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob) ON DELETE CASCADE,
    CHECK (vida_jogador_atual >= 0),
    CHECK (vida_inimigo_atual >= 0),
    CHECK (turno_atual IN ('jogador', 'inimigo')),
    CHECK (status_combate IN ('ativo', 'finalizado', 'fugiu'))
);

-- Tabela para registrar log detalhado das ações do combate
CREATE TABLE IF NOT EXISTS Combate_Log (
    id_log INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_combate INT NOT NULL,
    turno_numero INT NOT NULL,
    ator VARCHAR(10) NOT NULL, -- 'jogador' ou 'inimigo'
    acao VARCHAR(20) NOT NULL, -- 'ataque', 'defesa', 'fuga', 'habilidade'
    dano_causado INT DEFAULT 0,
    vida_restante_jogador INT NOT NULL,
    vida_restante_inimigo INT NOT NULL,
    descricao_acao TEXT,
    timestamp_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_combate) REFERENCES Combate(id_combate) ON DELETE CASCADE,
    CHECK (dano_causado >= 0),
    CHECK (vida_restante_jogador >= 0),
    CHECK (vida_restante_inimigo >= 0),
    CHECK (ator IN ('jogador', 'inimigo')),
    CHECK (acao IN ('ataque', 'defesa', 'fuga', 'habilidade', 'inicio'))
);

-- Tabela para registrar resultados finais dos combates
CREATE TABLE IF NOT EXISTS Combate_Resultado (
    id_resultado INT GENERATED ALWAYS AS IDENTITY (START WITH 1) PRIMARY KEY,
    id_combate INT NOT NULL UNIQUE,
    vencedor VARCHAR(10) NOT NULL, -- 'jogador', 'inimigo', 'fuga'
    xp_ganho INT DEFAULT 0,
    gcs_ganho INT DEFAULT 0,
    itens_dropados TEXT, -- JSON ou lista de itens ganhos
    duracao_combate INTERVAL,
    total_turnos INT DEFAULT 0,
    dano_total_jogador INT DEFAULT 0,
    dano_total_inimigo INT DEFAULT 0,
    FOREIGN KEY (id_combate) REFERENCES Combate(id_combate) ON DELETE CASCADE,
    CHECK (vencedor IN ('jogador', 'inimigo', 'fuga')),
    CHECK (xp_ganho >= 0),
    CHECK (gcs_ganho >= 0),
    CHECK (total_turnos >= 0),
    CHECK (dano_total_jogador >= 0),
    CHECK (dano_total_inimigo >= 0)
);

-- Índices para melhorar performance das consultas
CREATE INDEX IF NOT EXISTS idx_combate_player ON Combate(id_player);
CREATE INDEX IF NOT EXISTS idx_combate_status ON Combate(status_combate);
CREATE INDEX IF NOT EXISTS idx_combate_log_combate ON Combate_Log(id_combate);
CREATE INDEX IF NOT EXISTS idx_combate_resultado_combate ON Combate_Resultado(id_combate);

-- Comentários para documentação
COMMENT ON TABLE Combate IS 'Registra combates ativos entre jogadores e inimigos';
COMMENT ON TABLE Combate_Log IS 'Log detalhado de todas as ações durante um combate';
COMMENT ON TABLE Combate_Resultado IS 'Resultados finais e estatísticas dos combates concluídos';

COMMENT ON COLUMN Combate.turno_atual IS 'Indica de quem é o turno atual no combate';
COMMENT ON COLUMN Combate.status_combate IS 'Status atual do combate (ativo, finalizado, fugiu)';
COMMENT ON COLUMN Combate_Log.acao IS 'Tipo de ação realizada (ataque, defesa, fuga, habilidade)';
COMMENT ON COLUMN Combate_Resultado.vencedor IS 'Quem venceu o combate (jogador, inimigo, fuga)';
COMMENT ON COLUMN Combate_Resultado.itens_dropados IS 'Lista de itens obtidos após vitória (formato JSON)';
