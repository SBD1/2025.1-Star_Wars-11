# Módulo 3 - Integridade e Otimização do Sistema

## Visão Geral

O Módulo 3 do projeto Star Wars MUD concentra-se na garantia de integridade do banco de dados, otimização de performance e implementação de sistemas automatizados através de procedures, triggers e mecanismos de generalização/especialização.

## Objetivos do Módulo

- Implementar procedures para lógicas complexas do jogo
- Desenvolver triggers para automação de processos
- Criar sistema de generalização/especialização para entidades
- Otimizar queries e índices
- Garantir integridade referencial e consistência dos dados

## Componentes do Módulo

### 1. Procedures Implementadas

**Sistema de Combate:**
```sql
CREATE OR REPLACE PROCEDURE processar_combate(
    p_id_player INTEGER,
    p_id_inimigo INTEGER
) LANGUAGE plpgsql AS $$
BEGIN
    -- Cálculos de dano
    -- Gerenciamento de vida/energia
    -- Distribuição de experiência
END; $$;
```

**Sistema de Missões:**
```sql
CREATE OR REPLACE PROCEDURE gerenciar_missao_boss(
    p_id_player INTEGER,
    p_id_missao INTEGER
) LANGUAGE plpgsql AS $$
BEGIN
    -- Verificação de requisitos
    -- Controle de objetivos
    -- Distribuição de recompensas
END; $$;
```

**Gerenciamento de Inventário:**
```sql
CREATE OR REPLACE PROCEDURE atualizar_inventario(
    p_id_player INTEGER,
    p_id_item INTEGER
) LANGUAGE plpgsql AS $$
BEGIN
    -- Atualização pós-combate
    -- Sistema de compra/venda
    -- Controle de equipamentos
END; $$;
```

### 2. Triggers Implementados

**Conclusão de Missões:**
```sql
CREATE OR REPLACE TRIGGER after_mission_complete
    AFTER UPDATE ON Missao
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_status_missao();
```

**Atualização de Inventário:**
```sql
CREATE OR REPLACE TRIGGER after_combat_victory
    AFTER UPDATE ON Combate
    FOR EACH ROW
    EXECUTE FUNCTION processar_loot();
```

**Status do Personagem:**
```sql
CREATE OR REPLACE TRIGGER after_xp_gain
    AFTER UPDATE ON Personagem
    FOR EACH ROW
    EXECUTE FUNCTION atualizar_nivel();
```

### 3. Sistema de Generalização/Especialização

**Hierarquia de Inimigos:**
```sql
CREATE TABLE Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    nivel INTEGER,
    tipo VARCHAR(50)
);

CREATE TABLE Inimigo_Normal (
    id_inimigo INTEGER PRIMARY KEY REFERENCES Inimigo(id_inimigo),
    drop_chance DECIMAL
);

CREATE TABLE Inimigo_Elite (
    id_inimigo INTEGER PRIMARY KEY REFERENCES Inimigo(id_inimigo),
    bonus_dano INTEGER,
    resistencia INTEGER
);

CREATE TABLE Boss (
    id_inimigo INTEGER PRIMARY KEY REFERENCES Inimigo(id_inimigo),
    mecanica_especial TEXT,
    pre_requisito INTEGER
);
```

**Classes de Personagem:**
```sql
CREATE TABLE Classe (
    id_classe SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    descricao TEXT
);

CREATE TABLE Jedi (
    id_classe INTEGER PRIMARY KEY REFERENCES Classe(id_classe),
    poder_forca INTEGER,
    sabedoria INTEGER
);

CREATE TABLE Sith (
    id_classe INTEGER PRIMARY KEY REFERENCES Classe(id_classe),
    poder_escuro INTEGER,
    corrupcao INTEGER
);
```

### 4. Otimização de Performance

**Índices Implementados:**
```sql
CREATE INDEX idx_personagem_nivel ON Personagem(nivel);
CREATE INDEX idx_missao_status ON Missao(status);
CREATE INDEX idx_inventario_player ON Inventario(id_player);
```

**Views Otimizadas:**
```sql
CREATE MATERIALIZED VIEW view_status_personagem AS
SELECT p.id_player, p.nivel, i.quantidade_itens, m.missoes_completas
FROM Personagem p
LEFT JOIN Inventario i ON p.id_player = i.id_player
LEFT JOIN Missao m ON p.id_player = m.id_player;
```

### 5. Integridade de Dados

**Constraints Implementadas:**
```sql
ALTER TABLE Personagem
ADD CONSTRAINT check_nivel
CHECK (nivel BETWEEN 1 AND 100);

ALTER TABLE Inventario
ADD CONSTRAINT check_quantidade
CHECK (quantidade >= 0);
```

## Melhorias de Sistema

### 1. Sistema de Logs
- Registro de ações importantes
- Tracking de mudanças no banco
- Monitoramento de performance

### 2. Backup e Recuperação
- Backup automático diário
- Sistema de restore pontual
- Verificação de integridade

### 3. Segurança
- Controle de acesso por roles
- Criptografia de dados sensíveis
- Validação de inputs

## Resultados Alcançados

### Performance
- Redução no tempo de resposta de queries
- Otimização de procedures complexas
- Melhor utilização de recursos

### Integridade
- Garantia de consistência dos dados
- Automação de processos críticos
- Sistema robusto de validações

## Documentação Técnica

### Procedures
- Documentação detalhada de cada procedure
- Fluxogramas de processos
- Casos de uso e exemplos

### Triggers
- Descrição de cada trigger
- Condições de ativação
- Ações executadas

## Conclusão

O Módulo 3 estabeleceu uma base sólida para a integridade e performance do sistema, implementando mecanismos automatizados e garantindo a consistência dos dados através de procedures, triggers e especializações bem definidas.

## Histórico de Versões

| Versão | Data       | Modificações                               | Autor(es)     | Revisor(es) |
|--------|------------|-------------------------------------------|---------------|-------------|
| 1.0    | 04/08/2025 | DOcumentação técnica do módulo 3          | [Artur Mendonça](https://github.com/ArtyMend07) | [Filipe Bressanelli](https://github.com/fbressa) |