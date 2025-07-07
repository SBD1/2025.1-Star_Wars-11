<h1 align="center">
    <img src="https://github.com/SBD1/2025.1-Star_Wars-11/blob/main/docs/Imagens/StarWarsIcon.png" height="250px"alt="Logo">
</h1>

Repositório para desenvolvimento do jogo Star Wars da disciplina de SBD1 - 2025.1

## Sumário

- [Sobre o Jogo](#sobre-o-jogo)
- [Pré-requisitos](#pré-requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Módulos do Projeto](#módulos-do-projeto)
- [Documentação Online](#documentação-online)
- [Histórico de Versões](#histórico-de-versões)


# Sobre o Jogo:

O jogo é ambientado no universo de Star Wars e segue o estilo MUD, com interações baseadas em texto. O jogador cria um personagem, escolhendo uma classe (como Jedi, Sith ou Caçador de Recompensas), e inicia sua jornada em um planeta dentro de um sistema estelar. Ao longo da aventura, pode aceitar missões, viajar entre planetas usando diferentes tipos de naves e coletar itens como armas, armaduras e artefatos.

As missões são ligadas a planetas específicos e oferecem recompensas e desafios variados. O progresso de cada missão é registrado individualmente, permitindo acompanhar objetivos pendentes e concluídos. O jogador também gerencia um inventário de itens e uma frota de naves, que influenciam na exploração e combate.

Todo o funcionamento do jogo é estruturado em um banco de dados relacional que armazena informações sobre o personagem, planetas, naves, itens e missões, garantindo organização e continuidade na jogabilidade.

## Integrantes:

<table>
    <tr>
    <td align="center"><a href="https://github.com/ArtyMend07"><img src="https://avatars.githubusercontent.com/u/121322804?v=4" width="200px;" alt=""/><br/><sub><b>Artur Mendonça</b></sub></a><br/>
    <td align="center"><a href="https://github.com/Edumorais08"><img src="https://avatars.githubusercontent.com/u/139409504?v=4" width="200px;" alt=""/><br /><sub><b>Eduardo Morais</b></sub></a><br />
    <td align="center"><a href="https://github.com/fbressa"><img src="https://avatars.githubusercontent.com/u/123025849?v=4" width="200px;" alt=""/><br /><sub><b>Filipe Bressanelli</b></sub></a><br />
    <td align="center"><a href="https://github.com/Amandaaaaabreu"><img src="https://avatars.githubusercontent.com/u/103958998?v=4" width="200px;" alt=""/><br /><sub><b>Amanda Abreu</b></sub></a><br />
    <td align="center"><a href="https://github.com/renanpariiz"><img src="https://avatars.githubusercontent.com/u/101299192?v=4" width="200px;" alt=""/><br /><sub><b>Renan Pariz</b></sub></a><br />
    </tr>
</table>

## Como Executar o Projeto

### Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/)
- [PgAdmin4](https://www.pgadmin.org/download/) (opcional)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/SBD1/2025.1-Star_Wars-11.git
cd 2025.1-Star_Wars-11
```

2. **Inicie os containers**
```bash
docker compose up -d
```

3. Instalando Pacotes Python 

```bash
pip install -r requirements.txt
```

3. **Conecte ao banco via PgAdmin**
- Host: localhost
- Port: 5433
- Database: star_wars_db
- Username: postgres
- Password: postgres

### 📝 Documentação Completa

Para instruções detalhadas, consulte nossa [documentação de setup](docs/setup/setup_projeto.md).

## Estrutura do Projeto
```
.
├── src/                          # Código fonte
│   ├── DDL/                     # Data Definition Language - Estruturas do BD
│   │   ├── ddl_sistema.sql     # Sistema estelar
│   │   ├── ddl_planeta.sql     # Planetas
│   │   ├── ddl_personagem.sql  # Classes e personagens
│   │   ├── ddl_npcs.sql       # NPCs do jogo
│   │   ├── ddl_missao.sql     # Sistema de missões
│   │   ├── ddl_nave.sql       # Naves espaciais
│   │   ├── ddl_mobs.sql       # Inimigos
│   │   ├── ddl_inventario_jogador.sql  # Inventário
│   │   ├── ddl_funcoes_missoes.sql     # Funções de missões
│   │   └── ddl_triggers.sql            # Triggers automáticos
│   ├── DML/                     # Data Manipulation Language - Dados iniciais
│   │   ├── dml_personagem.sql
│   │   ├── dml_nave.sql
│   │   ├── dml_inventario_jogador.sql
│   │   ├── dml_classes_especializadas.sql
│   │   ├── dml_missao.sql
│   │   ├── dml_mobs.sql
│   │   ├── dml_npcs.sql
│   │   └── dml_sistema_planeta.sql
│   ├── DQL/                     # Data Query Language - Consultas
│   │   ├── dql_personagem_classe_planeta.sql
│   │   ├── dql_planeta.sql
│   │   ├── dql_sistema.sql
│   │   ├── dql_nave.sql
│   │   ├── dql_missao.sql
│   │   ├── dql_npc.sql
│   │   └── dql_inventario.sql
│   ├── MUD/                     # Aplicação do jogo
│   │   └── jogo_starwars.py    # Lógica principal do MUD
│   ├── migracoes/              # Sistema de migrações
│   │   ├── alembic/           # Configurações Alembic
│   │   └── alembic.ini        # Arquivo de configuração
│   └── main.py                 # Ponto de entrada da aplicação
├── docs/                        # Documentação completa
│   ├── modulo_1.md            # Documentação do Módulo 1 - Modelagem
│   ├── modulo_2.md            # Documentação do Módulo 2 - SQL
│   ├── atas/                   # Registros de reuniões
│   ├── backlog/               # Planejamento e backlog
│   ├── gravacoes/            # Links das apresentações
│   ├── Imagens/              # Recursos visuais
│   ├── implementacao/        # Documentação técnica
│   ├── jogo/                 # Documentação do jogo
│   ├── metodologia/          # Processo de desenvolvimento
│   ├── modelagens/           # MER, Modelo Relacional e Dicionário
│   └── setup/                # Guias de instalação e configuração
├── index.html                  # GitHub Pages - Interface web
├── docker-compose.yml         # Configuração Docker
├── Dockerfile                # Build da aplicação
└── requirements.txt          # Dependências Python
```

## Módulos do Projeto

### 📚 Módulo 1 - Modelagem de Dados
Abrange toda a fase de modelagem conceitual e lógica do banco de dados:
- **Modelo Entidade-Relacionamento (MER)**: Estrutura conceitual
- **Modelo Relacional**: Conversão para estrutura relacional
- **Dicionário de Dados**: Documentação completa das estruturas

### 📚 Módulo 2 - Implementação e Desenvolvimento
Implementação física do banco e desenvolvimento do jogo:
- **DDL**: Criação das estruturas físicas do banco
- **DML**: Inserção de dados iniciais do universo Star Wars
- **DQL**: Consultas otimizadas para o jogo
- **Migrações**: Controle de versão do banco de dados
- **Jogo MUD**: Aplicação inicial com interface de texto

## Documentação Online

Acesse nossa documentação completa em: [Star Wars MUD - Documentação](https://sbd1.github.io/2025.1-Star_Wars-11/)

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Estruturação completa da README         | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) |