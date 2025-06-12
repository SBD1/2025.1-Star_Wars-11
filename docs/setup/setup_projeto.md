# 🚀 Guia de Configuração e Execução do Projeto

## Pré-requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)
- [PgAdmin4](https://www.pgadmin.org/download/) (opcional, para visualização do banco)

## 1. Clone do Repositório

```bash
git clone https://github.com/SBD1/2025.1-Star_Wars-11.git
cd 2025.1-Star_Wars-11
```

## 2. Configuração do Ambiente

O projeto utiliza Docker para garantir um ambiente consistente. A estrutura inclui:

- **PostgreSQL**: Banco de dados principal (porta 5433)
- **Python**: Aplicação CLI (com psycopg2 para conexão)

## 3. Execução do Projeto

### 3.1. Iniciando os Containers

```bash
docker-compose up -d
```

Este comando:
- Cria e inicia os containers do PostgreSQL e da aplicação
- Executa os scripts SQL de criação das tabelas (DDL)
- Insere dados iniciais (DML)

### 3.2. Verificando os Logs

```bash
docker-compose logs -f
```

### 3.3. Parando os Containers

```bash
docker-compose down
```

Para remover também os volumes:
```bash
docker-compose down -v
```

## 4. Conexão com o Banco de Dados

### 4.1. Via PgAdmin

1. Abra o PgAdmin
2. Adicione um novo servidor com:
   - Host: localhost
   - Port: 5433
   - Database: star_wars_db
   - Username: postgres
   - Password: postgres

### 4.2. Via Terminal

```bash
psql -h localhost -p 5433 -U postgres -d star_wars_db
```

## 5. Estrutura do Projeto

```
.
├── src/
│   ├── DDL/               # Scripts de criação das tabelas
│   ├── DML/               # Scripts de inserção de dados
│   └── main.py           # Aplicação principal
├── docker-compose.yml    # Configuração dos containers
└── Dockerfile           # Configuração da imagem Python
```

## 6. Solução de Problemas

### 6.1. Porta 5433 em uso

Se a porta 5433 estiver em uso:
1. Verifique processos: `netstat -an | findstr 5433`
2. Encerre o processo ou
3. Mude a porta no docker-compose.yml

### 6.2. Falha na Conexão

Se houver falha na conexão:
1. Verifique se os containers estão rodando: `docker ps`
2. Verifique os logs: `docker-compose logs`
3. Reinicie os containers: `docker-compose restart`


## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 12/06/2025 | Criação do documento de setup do projeto          | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |