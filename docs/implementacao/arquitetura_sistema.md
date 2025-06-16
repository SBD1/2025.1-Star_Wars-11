# Arquitetura do Sistema - Star Wars MUD

## 🏗️ Visão Geral da Arquitetura

O Star Wars MUD segue uma arquitetura em camadas com separação clara de responsabilidades, utilizando Python para a lógica de aplicação e PostgreSQL para persistência de dados.

## 📊 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Terminal UI   │  │   Web Interface │  │  Documentation│ │
│  │   (main.py)     │  │   (index.html)  │  │   (Markdown) │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APLICAÇÃO                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Game Logic     │  │  Connection     │  │   Validation │ │
│  │ (jogo_starwars) │  │   Manager       │  │    Rules     │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE DADOS                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   PostgreSQL    │  │    Alembic      │  │    Docker    │ │
│  │   Database      │  │   Migrations    │  │  Container   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Componentes do Sistema

### 1. Camada de Apresentação

#### Terminal Interface (`src/main.py`)
- **Responsabilidade**: Interface de linha de comando
- **Tecnologia**: Python CLI
- **Funcionalidades**:
  - Gerenciamento de conexão com banco
  - Menu principal de navegação
  - Tratamento de entrada do usuário

#### Web Interface (`index.html`)
- **Responsabilidade**: Documentação interativa
- **Tecnologia**: HTML5, Bootstrap, JavaScript
- **Funcionalidades**:
  - Visualização de documentação
  - Navegação entre seções
  - Renderização de Markdown

### 2. Camada de Aplicação

#### Game Logic (`src/MUD/jogo_starwars.py`)
- **Responsabilidade**: Lógica principal do jogo
- **Padrão**: MVC (Model-View-Controller)
- **Funcionalidades**:
  - Gerenciamento de personagens
  - Sistema de viagem
  - Validação de regras de negócio

```python
class JogoStarWars:
    def __init__(self, conexao):
        self.conexao = conexao
        self.jogador_atual = None
    
    def iniciar(self):
        # Loop principal do jogo
    
    def criar_personagem(self):
        # Lógica de criação
    
    def viajar_para_planeta(self, destino, nave):
        # Sistema de viagem
```

#### Connection Manager
- **Responsabilidade**: Gerenciamento de conexões
- **Tecnologia**: psycopg2
- **Funcionalidades**:
  - Pool de conexões
  - Retry automático
  - Detecção de ambiente (local/container)

### 3. Camada de Dados

#### PostgreSQL Database
- **Versão**: PostgreSQL 17.5
- **Encoding**: UTF-8
- **Funcionalidades**:
  - Armazenamento relacional
  - Integridade referencial
  - Transações ACID

#### Alembic Migrations
- **Responsabilidade**: Versionamento do schema
- **Localização**: `src/migracoes/`
- **Funcionalidades**:
  - Criação automática de tabelas
  - Versionamento de mudanças
  - Rollback de migrações

## 🐳 Containerização

### Docker Compose Services

```yaml
services:
  db:                    # PostgreSQL Database
    image: postgres:latest
    ports: ["5433:5432"]
    
  migracoes:            # Schema Management
    build: .
    command: alembic upgrade head
    depends_on: [db]
```

### Benefícios da Containerização
- **Isolamento**: Ambiente consistente
- **Portabilidade**: Execução em qualquer sistema
- **Escalabilidade**: Fácil replicação
- **Desenvolvimento**: Setup simplificado

## 🔄 Fluxo de Dados

### 1. Inicialização do Sistema
```
1. Docker Compose inicia PostgreSQL
2. Alembic executa migrações
3. Python conecta ao banco
4. Interface de usuário é apresentada
```

### 2. Criação de Personagem
```
1. Usuário escolhe classe e planeta
2. Validação de entrada
3. Inserção no banco (Personagem)
4. Criação automática de nave (Trigger)
5. Confirmação para o usuário
```

### 3. Sistema de Viagem
```
1. Consulta naves do jogador
2. Lista planetas disponíveis
3. Validação de requisitos
4. Atualização de localização
5. Confirmação de viagem
```

## 🔒 Segurança e Validação

### Validação de Entrada
- **SQL Injection**: Uso de prepared statements
- **Tipo de Dados**: Validação antes de inserção
- **Integridade**: Foreign keys no banco

### Tratamento de Erros
```python
try:
    cursor.execute(query, params)
    conexao.commit()
except Exception as erro:
    print(f"Erro: {erro}")
    conexao.rollback()
```

### Transações
- **Atomicidade**: Operações completas ou revertidas
- **Consistência**: Estado válido sempre mantido
- **Isolamento**: Transações independentes

## 📈 Performance e Otimização

### Índices Recomendados
```sql
-- Consultas por jogador
CREATE INDEX idx_nave_player ON Nave(Id_Player);

-- Consultas por localização
CREATE INDEX idx_personagem_planeta ON Personagem(nome_planeta);

-- Consultas por classe
CREATE INDEX idx_personagem_classe ON Personagem(nome_classe);
```

## 🛠️ Ferramentas de Desenvolvimento

### Ambiente Local
```bash
# Desenvolvimento
python src/main.py

# Testes
pytest tests/

# Migrações
alembic upgrade head
```

### CI/CD (Futuro)
```yaml
# .github/workflows/ci.yml
- name: Test Database
  run: |
    docker-compose up -d db
    python -m pytest tests/
```

## 📚 Padrões Utilizados

### Design Patterns
- **Singleton**: Conexão com banco
- **Factory**: Criação de personagens
- **Strategy**: Diferentes tipos de nave

### Convenções de Código
- **PEP 8**: Estilo Python
- **SQL**: Nomes em snake_case
- **Documentação**: Docstrings em português

---

## 🔍 Análise de Qualidade

### Métricas de Código
- **Complexidade**: Baixa (funções < 20 linhas)
- **Acoplamento**: Mínimo entre módulos
- **Coesão**: Alta dentro de classes

### Manutenibilidade
- **Separação de responsabilidades**: ✅
- **Documentação**: ✅
- **Testes**: 🔄 Em desenvolvimento
- **Versionamento**: ✅
