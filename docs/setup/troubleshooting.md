# Troubleshooting - Star Wars MUD

## 🚨 Problemas Comuns e Soluções

Este documento lista os problemas mais frequentes e suas soluções para o Star Wars MUD.

## 🔌 Problemas de Conexão

### ❌ Erro: "could not translate host name 'db'"

**Sintomas**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe3 in position 58
could not translate host name "db" to address: Este host não é conhecido.
```

**Causa**: Executando Python fora do container Docker

**Solução**:
```bash
# Opção 1: Executar dentro do container
docker exec -it [container-name]-app-1 python src/main.py

# Opção 2: Usar configuração local (já implementado)
python src/main.py  # Conecta automaticamente via localhost:5433
```

**Verificação**:
```bash
# Confirmar que containers estão rodando
docker ps

# Deve mostrar:
# - postgres container na porta 5433
```

### ❌ Erro: "Connection refused"

**Sintomas**:
```
psycopg2.OperationalError: connection to server at "localhost", port 5433 failed
```

**Causa**: Containers não estão rodando

**Solução**:
```bash
# Iniciar containers
docker-compose up -d

# Verificar status
docker-compose ps

# Aguardar healthcheck
docker-compose logs db
```

**Verificação**:
```bash
# Testar conexão direta
docker exec -it [container-name]-db-1 psql -U postgres -d star_wars_db -c "SELECT 1;"
```

### ❌ Erro: "Authentication failed"

**Sintomas**:
```
psycopg2.OperationalError: FATAL: password authentication failed for user "postgres"
```

**Causa**: Credenciais incorretas

**Solução**:
```bash
# Verificar variáveis de ambiente no docker-compose.yml
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: star_wars_db

# Recriar containers se necessário
docker-compose down -v
docker-compose up -d
```

## 🐳 Problemas com Docker

### ❌ Erro: "Port already in use"

**Sintomas**:
```
Error starting userland proxy: listen tcp 0.0.0.0:5433: bind: address already in use
```

**Causa**: Porta 5433 já está sendo usada

**Solução**:
```bash
# Verificar o que está usando a porta
netstat -tulpn | grep 5433

# Parar processo conflitante ou alterar porta
# No docker-compose.yml: "5434:5432"
```

### ❌ Erro: "No space left on device"

**Sintomas**:
```
Error response from daemon: no space left on device
```

**Causa**: Disco cheio

**Solução**:
```bash
# Limpar containers não utilizados
docker system prune -a

# Limpar volumes órfãos
docker volume prune

# Verificar espaço
df -h
```

### ❌ Erro: "Network not found"

**Sintomas**:
```
Error response from daemon: network [project]_default not found
```

**Causa**: Rede Docker corrompida

**Solução**:
```bash
# Recriar rede
docker-compose down
docker network prune
docker-compose up -d
```

## 🐍 Problemas com Python

### ❌ Erro: "ModuleNotFoundError: No module named 'psycopg2'"

**Sintomas**:
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Causa**: Dependência não instalada

**Solução**:
```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install psycopg2-binary
```

### ❌ Erro: "ModuleNotFoundError: No module named 'MUD'"

**Sintomas**:
```
ModuleNotFoundError: No module named 'MUD'
```

**Causa**: Executando de diretório incorreto

**Solução**:
```bash
# Navegar para o diretório correto
cd 2025.1-Star_Wars-11

# Executar a partir da raiz do projeto
python src/main.py
```

### ❌ Erro: "UnicodeDecodeError" (Windows)

**Sintomas**:
```
UnicodeDecodeError: 'charmap' codec can't decode byte
```

**Causa**: Encoding do terminal Windows

**Solução**:
```bash
# Configurar encoding UTF-8
set PYTHONIOENCODING=utf-8
python src/main.py

# Ou usar PowerShell
$env:PYTHONIOENCODING="utf-8"
python src/main.py
```

## 🎮 Problemas do Jogo

### ❌ Erro: "Personagem não encontrado"

**Sintomas**:
```
Personagem não encontrado!
```

**Causa**: ID incorreto ou personagem não existe

**Solução**:
```bash
# Verificar IDs existentes no banco
docker exec -it [container-name]-db-1 psql -U postgres -d star_wars_db -c "SELECT id_player, nome_classe FROM Personagem;"

# Criar novo personagem se necessário
```

### ❌ Erro: "foreign key constraint"

**Sintomas**:
```
insert or update on table "personagem" violates foreign key constraint
```

**Causa**: Classe ou planeta inválido

**Solução**:
```bash
# Verificar classes disponíveis
docker exec -it [container-name]-db-1 psql -U postgres -d star_wars_db -c "SELECT nome_classe FROM Classe;"

# Verificar planetas disponíveis
docker exec -it [container-name]-db-1 psql -U postgres -d star_wars_db -c "SELECT nome_planeta FROM Planeta;"

# Usar nomes exatos: "Jedi", "Sith", "Cacador_de_Recompensas"
```

### ❌ Erro: "Nave muito lenta"

**Sintomas**:
```
Sua nave é muito lenta para viajar para Coruscant!
```

**Causa**: Nave não atende requisitos de velocidade

**Solução**:
```bash
# Verificar velocidade da nave
# Coruscant requer velocidade ≥ 150
# Tatooine requer velocidade ≥ 100

# Usar nave adequada ou escolher outro destino
```

## 🗄️ Problemas de Banco de Dados

### ❌ Erro: "relation does not exist"

**Sintomas**:
```
psycopg2.errors.UndefinedTable: relation "personagem" does not exist
```

**Causa**: Migrações não executadas

**Solução**:
```bash
# Executar migrações manualmente
docker exec -it [container-name]-migracoes-1 alembic upgrade head

# Ou recriar containers
docker-compose down
docker-compose up -d
```

### ❌ Erro: "Database does not exist"

**Sintomas**:
```
psycopg2.OperationalError: database "star_wars_db" does not exist
```

**Causa**: Banco não foi criado

**Solução**:
```bash
# Recriar containers com volumes limpos
docker-compose down -v
docker-compose up -d

# Aguardar inicialização completa
docker-compose logs -f db
```

### ❌ Erro: "Too many connections"

**Sintomas**:
```
psycopg2.OperationalError: FATAL: too many clients already
```

**Causa**: Muitas conexões abertas

**Solução**:
```bash
# Reiniciar container do banco
docker-compose restart db

# Verificar conexões ativas
docker exec -it [container-name]-db-1 psql -U postgres -d star_wars_db -c "SELECT count(*) FROM pg_stat_activity;"
```

## 🔧 Ferramentas de Diagnóstico


### Logs Úteis

```bash
# Logs do banco de dados
docker-compose logs db

# Logs das migrações
docker-compose logs migracoes

# Logs em tempo real
docker-compose logs -f

# Logs específicos
docker logs [container-id]
```

### Comandos de Reset

```bash
# Reset completo (CUIDADO: apaga todos os dados)
docker-compose down -v
docker system prune -a
docker-compose up -d

# Reset apenas do banco
docker-compose down
docker volume rm [project]_postgres_data
docker-compose up -d
```

---

## 🎯 Dicas de Prevenção

1. **Sempre use `docker-compose up -d`** antes de executar o jogo
2. **Aguarde o healthcheck** do PostgreSQL antes de conectar
3. **Use nomes exatos** para classes e planetas
4. **Monitore logs** em caso de comportamento estranho
5. **Faça backup** de dados importantes antes de mudanças

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento de troubleshooting (solução de problemas)          | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |