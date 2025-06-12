
# 📋 Backlog Técnico — Star Wars MUD (SQL + Python CLI)

As tarefas estão organizadas em **ordem de execução recomendada**.

---

## 🧱 1. BANCO DE DADOS – Estrutura Inicial

### 📌 Etapa 1 – Fundamentação do modelo
- [ ] Adicionar campo `senha` na tabela `personagem` (para login)
- [ ] Adicionar campos `nivel`, `vida`, `energia`, `xp` na tabela `personagem`
- [ ] Criar tabela `item`
  - Campos: `id`, `nome`, `tipo`, `efeito`, `valor`, `peso`
- [ ] Garantir que `inventario_jogador` tenha FK para `item`
- [ ] Criar tabela `personagem_missao`
  - Campos: `id_personagem`, `id_missao`, `status`, `data_inicio`, `data_conclusao`
- [ ] Criar tabela `nave_personagem` (múltiplas naves por jogador)
  - Campos: `id_personagem`, `id_nave`

### 📌 Etapa 2 – Enriquecimento do universo
- [ ] Adicionar atributos a `mobs`: `vida`, `ataque`, `defesa`, `xp_dado`, `planeta_id`
- [ ] Associar NPCs a planetas e missões

---

## 🧠 2. BACKEND EM PYTHON – Desenvolvimento Modular

### 🔧 Etapa 3 – Conexão e base do sistema
- [ ] Criar conexão com banco usando `psycopg2` e `.env`
- [ ] Criar módulo `database.py` para facilitar as queries

### 👤 Etapa 4 – Sistema de usuário e personagem
- [ ] Criar função `cadastrar_personagem()`
- [ ] Criar função `login_personagem()`
- [ ] Criar função `ver_status_personagem()`

### 🌌 Etapa 5 – Missões e movimentação
- [ ] Função `listar_missoes_disponiveis(id_personagem)`
- [ ] Função `aceitar_missao(id_personagem, id_missao)`
- [ ] Função `viajar_para_planeta(id_personagem, planeta_destino)`
- [ ] Função `concluir_missao(id_personagem, id_missao)`

### 📦 Etapa 6 – Inventário
- [ ] Função `ver_inventario(id_personagem)`
- [ ] Função `usar_item(id_personagem, item_id)`

### ⚔️ Etapa 7 – Combate (opcional)
- [ ] Função `iniciar_combate(id_personagem, mob_id)`
- [ ] Função `registrar_dano_e_status`

---

## 💻 3. TERMINAL CLI – Integração com Jogador

### 🧩 Etapa 8 – Interface de comandos
- [ ] Comando: `!cadastrar`
- [ ] Comando: `!login`
- [ ] Comando: `!sair`
- [ ] Comando: `!status` – ver status do personagem
- [ ] Comando: `!viajar <planeta>` – mover-se
- [ ] Comando: `!missões` – listar missões disponíveis
- [ ] Comando: `!aceitar <id_missao>` – aceitar missão
- [ ] Comando: `!concluir <id_missao>` – concluir missão
- [ ] Comando: `!inventario` – ver inventário
- [ ] Comando: `!usar <id_item>` – usar item
- [ ] Comando: `!ajuda` – mostrar todos os comandos

### 🛠 Etapa 9 – Extras e refinamentos
- [ ] Adicionar sistema de logs para registrar ações
- [ ] Criar função de salvar e carregar sessão (por ID de personagem)
