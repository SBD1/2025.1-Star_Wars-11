# Módulo 1 - Modelagem de Dados

## Visão Geral

O Módulo 1 do projeto Star Wars MUD abrange toda a fase de modelagem conceitual e lógica do banco de dados, incluindo a análise de requisitos, criação dos modelos de dados e documentação das estruturas que suportam o jogo.

## Objetivos do Módulo

- Definir a estrutura conceitual do banco de dados através do Modelo Entidade-Relacionamento (MER)
- Converter o modelo conceitual em um Modelo Relacional funcional
- Documentar todas as entidades, atributos e relacionamentos através do Dicionário de Dados
- Estabelecer as bases para a implementação física do banco de dados

## Componentes do Módulo

### 1. Modelo Entidade-Relacionamento (MER)

O MER representa a estrutura conceitual do banco de dados do jogo Star Wars MUD, definindo:

- **Entidades principais**: Personagem, Planeta, Sistema, Nave, Missão, NPC, Mob, Inventário
- **Relacionamentos**: Como as entidades se conectam e interagem
- **Cardinalidades**: Definição das regras de relacionamento entre entidades
- **Atributos**: Propriedades de cada entidade

**Principais entidades modeladas:**
- **Personagem**: Representa os jogadores e suas características
- **Planeta**: Localizações do universo Star Wars
- **Sistema**: Agrupamento de planetas
- **Nave**: Veículos espaciais dos personagens
- **Missão**: Tarefas e objetivos do jogo
- **NPC**: Personagens não-jogáveis
- **Mob**: Criaturas hostis
- **Inventário**: Itens dos personagens

### 2. Modelo Relacional

A conversão do MER para o modelo relacional, incluindo:

- **Tabelas**: Estruturas relacionais derivadas das entidades
- **Chaves primárias**: Identificadores únicos de cada tabela
- **Chaves estrangeiras**: Relacionamentos entre tabelas
- **Normalização**: Aplicação das formas normais para evitar redundâncias
- **Integridade referencial**: Garantia da consistência dos dados

**Principais tabelas:**
- `personagem`: Dados dos jogadores
- `planeta`: Informações dos planetas
- `sistema`: Sistemas estelares
- `nave`: Naves espaciais
- `missao`: Missões disponíveis
- `npc`: Personagens não-jogáveis
- `mob`: Criaturas do jogo
- `inventario_jogador`: Itens dos personagens

### 3. Dicionário de Dados

Documentação completa de todas as estruturas de dados, incluindo:

- **Descrição das tabelas**: Propósito e função de cada tabela
- **Especificação dos campos**: Tipo, tamanho, restrições e descrição
- **Relacionamentos**: Documentação das chaves estrangeiras
- **Regras de negócio**: Constraints e validações aplicadas
- **Índices**: Estruturas de otimização de consultas

## Metodologia Aplicada

### Análise de Requisitos
1. Levantamento das funcionalidades do jogo
2. Identificação das entidades do domínio
3. Definição dos relacionamentos
4. Especificação dos atributos

### Modelagem Conceitual
1. Criação do diagrama MER
2. Validação com as regras de negócio
3. Refinamento do modelo
4. Documentação das decisões de design

### Modelagem Lógica
1. Conversão do MER para modelo relacional
2. Aplicação das formas normais
3. Definição de chaves e índices
4. Validação da integridade referencial

## Ferramentas Utilizadas

- **Modelagem**: Ferramentas de diagramação para criação do MER
- **Documentação**: Markdown para documentação técnica
- **Validação**: Revisão por pares e validação com requisitos

## Resultados Obtidos

### Modelo Entidade-Relacionamento
- Diagrama completo com todas as entidades do jogo
- Relacionamentos bem definidos com cardinalidades corretas
- Atributos especificados com tipos e restrições

### Modelo Relacional
- Esquema relacional normalizado
- Estrutura otimizada para consultas do jogo
- Integridade referencial garantida

### Dicionário de Dados
- Documentação completa de todas as estruturas
- Especificações técnicas detalhadas
- Regras de negócio documentadas

## Validação e Qualidade

### Critérios de Validação
- Conformidade com os requisitos do jogo
- Aplicação correta das formas normais
- Integridade referencial mantida
- Documentação completa e clara

### Revisões Realizadas
- Revisão técnica do modelo
- Validação com as regras de negócio
- Verificação da documentação
- Testes de consistência

## Próximos Passos

O Módulo 1 estabelece as bases para o Módulo 2, que incluirá:
- Implementação física do banco de dados (DDL)
- Inserção de dados iniciais (DML)
- Criação de consultas (DQL)
- Desenvolvimento do jogo
- Configuração de migrações

## Conclusão

O Módulo 1 fornece uma base sólida para o desenvolvimento do Star Wars MUD, com modelos bem estruturados e documentação completa que facilitará a implementação e manutenção do sistema.

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento do módulo 1         | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) |

