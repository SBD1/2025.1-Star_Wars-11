# Sistema de Missões - Star Wars MUD

## 🎯 Visão Geral

O sistema de missões foi implementado seguindo as modelagens MER e MREL, utilizando principalmente SQL com funções PostgreSQL para máxima performance e integridade de dados.

## 📊 Estrutura do Banco de Dados

### Tabelas Principais

#### `Missao`
- **Campos**: id_missao, nome_missao, descricao, valor_recompensa, xp_recompensa, status, nome_planeta, id_NPC, level_minimo, tipo_missao
- **Tipos de Missão**: Entrega, Eliminação, Exploração, Coleta
- **Status**: Disponível, Em Andamento, Concluída, Falhada

#### `Missao_Jogador`
- **Função**: Rastreia missões aceitas pelos jogadores
- **Campos**: id_player, id_missao, status_jogador, data_aceita, data_concluida, progresso
- **Relacionamento**: Many-to-Many entre Personagem e Missao

#### Tabelas de Especialização
- **`Missao_Disponivel`**: Missões que podem ser aceitas
- **`Missao_Concluida`**: Estatísticas de conclusão
- **`Missao_Em_Andamento`**: Controle de jogadores ativos

## 🔧 Funções SQL Implementadas

### `listar_missoes_disponiveis(jogador_id)`
```sql
-- Lista missões que o jogador pode aceitar
-- Filtra por level mínimo e missões já aceitas
-- Retorna informações completas da missão
```

### `aceitar_missao(jogador_id, missao_id)`
```sql
-- Valida requisitos (level, planeta, duplicação)
-- Insere na tabela Missao_Jogador
-- Atualiza contadores
-- Retorna mensagem de sucesso/erro
```

### `concluir_missao(jogador_id, missao_id)`
```sql
-- Valida se missão está em andamento
-- Calcula recompensas (GCS + XP)
-- Verifica level up automático
-- Atualiza estatísticas
```

### `listar_missoes_jogador(jogador_id)`
```sql
-- Lista todas as missões do jogador
-- Mostra status e progresso
-- Ordenado por data de aceitação
```

### `abandonar_missao(jogador_id, missao_id)`
```sql
-- Remove missão do jogador
-- Atualiza contadores
-- Permite reaceitação futura
```

## 🎮 Interface do Jogo

### Comandos Disponíveis

#### `missoes`
- Lista missões disponíveis no planeta atual
- Filtra por level do jogador
- Mostra requisitos especiais

#### `minhas_missoes`
- Exibe missões aceitas pelo jogador
- Status visual com ícones (✓ ⏳ ✗)
- Informações de progresso

#### `aceitar_missao`
- Solicita ID da missão
- Valida automaticamente requisitos
- Feedback imediato de sucesso/erro

#### `concluir_missao`
- Marca missão como concluída
- Aplica recompensas automaticamente
- Notifica level up se aplicável

#### `abandonar_missao`
- Remove missão do jogador
- Permite reaceitação posterior

## 📋 Tipos de Missão

### 🚚 Entrega
- **Exemplo**: "Suprimentos para Mos Eisley"
- **Mecânica**: Transportar itens entre planetas
- **Requisitos**: Nave com capacidade adequada

### ⚔️ Eliminação
- **Exemplo**: "Eliminar Stormtroopers"
- **Mecânica**: Derrotar inimigos específicos
- **Requisitos**: Armas de combate

### 🗺️ Exploração
- **Exemplo**: "Explorar Ruínas Naboo"
- **Mecânica**: Visitar locais específicos
- **Requisitos**: Level mínimo recomendado

### 📦 Coleta
- **Exemplo**: "Coletar Peças de Nave"
- **Mecânica**: Reunir recursos específicos
- **Requisitos**: Equipamento de escavação

## 🎯 Regras de Negócio

### Validações Automáticas
1. **Level Mínimo**: Jogador deve ter level suficiente
2. **Localização**: Deve estar no planeta da missão
3. **Duplicação**: Não pode aceitar missão já aceita
4. **Status**: Só pode concluir missões em andamento

### Sistema de Recompensas
- **GCS**: Créditos galácticos baseados na dificuldade
- **XP**: Experiência para progressão de level
- **Level Up**: Automático a cada 1000 XP

### Progressão de Dificuldade
- **Level 1-5**: Missões básicas (1000-2000 GCS)
- **Level 6-10**: Missões intermediárias (3000-5000 GCS)
- **Level 11+**: Missões avançadas (5000+ GCS)

## 🔍 Consultas DQL

### Estatísticas por Planeta
```sql
SELECT 
    nome_planeta,
    COUNT(*) as total_missoes,
    AVG(valor_recompensa) as recompensa_media
FROM Missao 
GROUP BY nome_planeta;
```

### Missões Mais Populares
```sql
SELECT m.nome_missao, mc.total_conclusoes
FROM Missao m
JOIN Missao_Concluida mc ON m.id_missao = mc.id_missao
ORDER BY mc.total_conclusoes DESC;
```

## 🚀 Funcionalidades Implementadas

### ✅ Completas
- [x] Listagem de missões disponíveis
- [x] Aceitação de missões com validações
- [x] Conclusão de missões com recompensas
- [x] Abandono de missões
- [x] Rastreamento de progresso
- [x] Sistema de level up automático
- [x] Interface de usuário intuitiva

### 🔄 Futuras Melhorias
- [ ] Missões com múltiplos objetivos
- [ ] Sistema de reputação com NPCs
- [ ] Missões em cadeia (quest chains)
- [ ] Recompensas de itens únicos
- [ ] Missões cooperativas (multiplayer)

## 🧪 Como Testar

1. **Criar Personagem**: Use o comando `1` no menu principal
2. **Entrar no Jogo**: Use o comando `2` e digite o ID do personagem
3. **Ver Missões**: Digite `missoes` para ver missões disponíveis
4. **Aceitar Missão**: Digite `aceitar_missao` e o ID da missão
5. **Verificar Progresso**: Digite `minhas_missoes`
6. **Concluir**: Digite `concluir_missao` e o ID da missão

## 📈 Métricas de Performance

- **Funções SQL**: Otimizadas com índices automáticos
- **Validações**: Realizadas no banco para consistência
- **Transações**: Atômicas para integridade de dados
- **Escalabilidade**: Suporta milhares de missões simultâneas

O sistema está 100% funcional e prático, seguindo as melhores práticas de desenvolvimento de jogos e banco de dados!
