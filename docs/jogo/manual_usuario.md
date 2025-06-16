# Manual do Usuário - Star Wars MUD

## 🎮 Introdução

Bem-vindo ao Star Wars MUD! Este é um jogo baseado em texto ambientado no universo de Star Wars, onde você pode criar personagens, explorar planetas e viver aventuras épicas.

## 🚀 Como Começar

### Pré-requisitos
- Docker e Docker Compose instalados
- Python 3.8+ (para execução local)

### Iniciando o Jogo
```bash
# 1. Clone o repositório
git clone https://github.com/SBD1/2025.1-Star_Wars-11.git
cd 2025.1-Star_Wars-11

# 2. Inicie o banco de dados
docker-compose up -d

# 3. Execute o jogo
python src/main.py
```

## 👤 Criação de Personagem

### Classes Disponíveis

#### 🗡️ Jedi
- **Especialidade**: Força e combate com sabre de luz
- **Habilidades**: Manipulação da Força, cura, proteção
- **Planeta Inicial Recomendado**: Coruscant

#### ⚡ Sith
- **Especialidade**: Lado sombrio da Força
- **Habilidades**: Ataques devastadores, manipulação mental
- **Planeta Inicial Recomendado**: Korriban

#### 🎯 Caçador de Recompensas
- **Especialidade**: Combate à distância e tecnologia
- **Habilidades**: Precisão, equipamentos avançados
- **Planeta Inicial Recomendado**: Tatooine

### Planetas Disponíveis

| Planeta | Clima | Características | Requisitos de Nave |
|---------|-------|-----------------|-------------------|
| **Tatooine** | Desértico | Planeta dos contrabandistas | Nenhum |
| **Coruscant** | Temperado | Capital da República | Velocidade ≥ 150 |
| **Naboo** | Temperado | Planeta pacífico | Nenhum |
| **Kashyyyk** | Tropical | Mundo dos Wookiees | Nenhum |
| **Hoth** | Gelado | Base rebelde | Nenhum |

## 🎯 Comandos do Jogo

### Menu Principal
- **1** - Criar personagem
- **2** - Carregar personagem
- **3** - Deletar personagem
- **4** - Sair

### Comandos Durante o Jogo
- **`status`** - Visualizar informações do personagem
- **`viajar`** - Viajar entre planetas
- **`missoes`** - Ver missões disponíveis (em desenvolvimento)
- **`sair`** - Voltar ao menu principal

## 🚀 Sistema de Viagem

### Naves Disponíveis

#### YT-1300 (Millennium Falcon)
- **Velocidade**: 145
- **Capacidade**: 5 passageiros
- **Disponível**: Por padrão para todos os jogadores

#### X-Wing T-65
- **Velocidade**: 120
- **Capacidade**: 1 piloto
- **Especialidade**: Combate

#### Lambda Class Shuttle
- **Velocidade**: 160
- **Capacidade**: 20 passageiros
- **Especialidade**: Transporte

### Requisitos de Viagem
- **Coruscant**: Requer nave com velocidade ≥ 150
- **Tatooine**: Requer nave com velocidade ≥ 100
- **Outros planetas**: Sem requisitos especiais

## 💡 Dicas para Iniciantes

### 1. Escolha da Classe
- **Jedi**: Ideal para jogadores que gostam de equilíbrio
- **Sith**: Para quem prefere poder ofensivo
- **Caçador**: Para estrategistas e amantes de tecnologia

### 2. Planeta Inicial
- **Tatooine**: Bom para iniciantes, sem restrições
- **Coruscant**: Mais desafiador, mas com mais oportunidades

### 3. Gerenciamento de Recursos
- **GCS (Galactic Credit Standard)**: Moeda do jogo
- **Vida**: Monitore sempre sua saúde
- **Level**: Aumenta com experiência

## 🔧 Solução de Problemas

### Erro de Conexão
```
Erro: 'utf-8' codec can't decode byte...
```
**Solução**: Certifique-se de que os containers estão rodando:
```bash
docker-compose up -d
```

### Personagem Não Encontrado
**Problema**: "Personagem não encontrado!"
**Solução**: Verifique se o ID está correto ou crie um novo personagem

### Nave Muito Lenta
**Problema**: "Sua nave é muito lenta para viajar..."
**Solução**: Use uma nave com velocidade adequada ou escolha outro destino

## 🎯 Próximas Funcionalidades

- Sistema de missões completo
- Combate entre personagens
- Inventário de itens
- Sistema de guilds
- Eventos especiais

---

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento do manual do usuário          | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |

