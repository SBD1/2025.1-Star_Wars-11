# Módulo 2 - Implementação e Desenvolvimento

## Visão Geral

O Módulo 2 do projeto Star Wars MUD abrange a implementação física do banco de dados e o desenvolvimento completo do jogo, incluindo a criação das estruturas de dados (DDL), inserção de dados iniciais (DML), consultas (DQL), sistema de migrações e a aplicação do jogo MUD.

## Objetivos do Módulo

- Implementar fisicamente o banco de dados baseado no modelo relacional
- Criar e popular as tabelas com dados iniciais do universo Star Wars
- Desenvolver consultas otimizadas para suportar as funcionalidades do jogo
- Implementar sistema de migrações para controle de versão do banco
- Desenvolver a aplicação do jogo MUD com interface de texto

## Componentes do Módulo

### 1. Data Definition Language (DDL)

Implementação das estruturas físicas do banco de dados:

**Arquivos DDL implementados:**
- `ddl_personagem.sql`: Criação da tabela de personagens
- `ddl_planeta.sql`: Estrutura dos planetas
- `ddl_sistema.sql`: Definição dos sistemas estelares
- `ddl_nave.sql`: Tabelas de naves espaciais
- `ddl_missao.sql`: Estrutura das missões
- `ddl_npcs.sql`: Definição dos NPCs
- `ddl_mobs.sql`: Criação das criaturas
- `ddl_inventario_jogador.sql`: Sistema de inventário
- `ddl_funcoes_missoes.sql`: Funções relacionadas às missões
- `ddl_triggers.sql`: Triggers para automação

**Características implementadas:**
- Criação de todas as tabelas do modelo relacional
- Definição de chaves primárias e estrangeiras
- Implementação de constraints e validações
- Criação de índices para otimização
- Triggers para automação de processos
- Funções personalizadas para lógica de negócio

### 2. Data Manipulation Language (DML)

Inserção e manipulação dos dados iniciais:

**Arquivos DML implementados:**
- `dml_personagem.sql`: Dados iniciais de personagens
- `dml_sistema_planeta.sql`: População de sistemas e planetas
- `dml_nave.sql`: Dados das naves disponíveis
- `dml_missao.sql`: Missões iniciais do jogo
- `dml_npcs.sql`: Personagens não-jogáveis
- `dml_mobs.sql`: Criaturas e inimigos
- `dml_inventario_jogador.sql`: Itens iniciais
- `dml_classes_especializadas.sql`: Classes de personagens

**Dados implementados:**
- Planetas icônicos do universo Star Wars
- Sistemas estelares conhecidos
- NPCs baseados em personagens da saga
- Missões inspiradas nos filmes e séries
- Itens e equipamentos temáticos
- Criaturas características de cada planeta

### 3. Data Query Language (DQL)

Consultas otimizadas para suportar o jogo:

**Arquivos DQL implementados:**
- `dql_personagem_classe_planeta.sql`: Consultas de personagens
- `dql_planeta.sql`: Informações dos planetas
- `dql_sistema.sql`: Dados dos sistemas
- `dql_nave.sql`: Consultas de naves
- `dql_missao.sql`: Busca de missões
- `dql_npc.sql`: Informações de NPCs
- `dql_inventario.sql`: Gestão de inventário

**Tipos de consultas:**
- Consultas básicas de seleção
- Joins complexos entre múltiplas tabelas
- Consultas agregadas para estatísticas
- Subconsultas para lógica avançada
- Views para simplificar consultas frequentes
- Consultas otimizadas para performance

### 4. Sistema de Migrações

Controle de versão e evolução do banco de dados:

**Estrutura implementada:**
- Configuração do Alembic para Python
- Scripts de migração versionados
- Controle de estado do banco
- Rollback de alterações
- Sincronização entre ambientes

**Funcionalidades:**
- Criação automática de migrações
- Aplicação incremental de mudanças
- Histórico de alterações
- Validação de integridade
- Backup automático antes de migrações

### 5. Aplicação do Jogo MUD

Desenvolvimento da interface e lógica do jogo:

**Arquivo principal:**
- `jogo_starwars.py`: Aplicação principal do MUD
- `main.py`: Ponto de entrada do sistema

**Funcionalidades implementadas:**
- Sistema de login e criação de personagens
- Navegação entre planetas e sistemas
- Sistema de combate contra mobs
- Interação com NPCs
- Sistema de missões
- Gerenciamento de inventário
- Comandos de jogo intuitivos
- Interface de texto imersiva

**Comandos disponíveis:**
- Movimentação: `ir`, `viajar`, `explorar`
- Combate: `atacar`, `fugir`, `usar_item`
- Interação: `falar`, `examinar`, `pegar`
- Inventário: `inventario`, `equipar`, `usar`
- Missões: `missoes`, `aceitar_missao`, `completar_missao`
- Sistema: `ajuda`, `status`, `sair`

## Arquitetura Técnica

### Tecnologias Utilizadas
- **Python**: Linguagem principal do jogo
- **PostgreSQL**: Sistema de gerenciamento de banco de dados
- **Alembic**: Sistema de migrações
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração dos serviços

### Estrutura do Projeto
```
src/
├── DDL/          # Scripts de criação de estruturas
├── DML/          # Scripts de inserção de dados
├── DQL/          # Scripts de consultas
├── MUD/          # Código do jogo
├── migracoes/    # Sistema de migrações
└── main.py       # Ponto de entrada
```

### Padrões Implementados
- Separação clara entre camadas de dados e aplicação
- Uso de SQL puro para máxima performance
- Código Python organizado e documentado
- Tratamento de erros e exceções
- Logging para debugging e monitoramento

## Integração e Deploy

### Containerização
- Dockerfile para a aplicação Python
- Docker Compose para orquestração
- Configuração de rede entre containers
- Volumes persistentes para dados

### Configuração de Ambiente
- Variáveis de ambiente para configuração
- Scripts de inicialização automática
- Backup e restore de dados
- Monitoramento de saúde dos serviços

## Testes e Validação

### Testes Implementados
- Validação das estruturas DDL
- Testes de integridade dos dados DML
- Performance das consultas DQL
- Funcionalidades do jogo MUD
- Sistema de migrações

### Critérios de Qualidade
- Integridade referencial mantida
- Performance adequada das consultas
- Interface de usuário intuitiva
- Tratamento adequado de erros
- Documentação completa

## Resultados Obtidos

### Banco de Dados
- Estrutura completa e funcional
- Dados iniciais consistentes
- Consultas otimizadas
- Sistema de migrações operacional

### Aplicação do Jogo
- Interface de texto imersiva
- Funcionalidades completas implementadas
- Sistema de combate balanceado
- Missões envolventes
- Navegação fluida entre planetas

## Documentação Complementar

### Manuais Disponíveis
- Manual do usuário para jogadores
- Regras de negócio detalhadas
- Lista completa de comandos
- Guia de troubleshooting
- Documentação técnica da arquitetura

## Conclusão

O Módulo 2 representa a materialização completa do projeto Star Wars MUD, transformando os modelos conceituais do Módulo 1 em uma aplicação funcional e envolvente. A implementação combina robustez técnica com uma experiência de jogo imersiva no universo Star Wars.

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento do módulo 2         | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) |
