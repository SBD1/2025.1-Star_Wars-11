# Comandos Disponíveis - Star Wars MUD

## 📋 Visão Geral

Este documento lista todos os comandos disponíveis no Star Wars MUD, organizados por contexto e funcionalidade.

## 🏠 Menu Principal

### Comandos Numéricos

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `1` | Criar novo personagem | Digite `1` e siga as instruções |
| `2` | Carregar personagem existente | Digite `2` e informe o ID |
| `3` | Deletar personagem | Digite `3` e confirme o ID |
| `4` | Sair do jogo | Digite `4` para encerrar |

### Fluxo de Criação de Personagem

```
=== Criação de Personagem ===

Classes disponíveis:
- Jedi
- Sith
- Cacador_de_Recompensas

Planetas disponíveis:
- Tatooine
- Coruscant
- Naboo
- Kashyyyk
- Hoth

Escolha sua classe: [Digite o nome exato]
Escolha seu planeta inicial: [Digite o nome exato]
```

### Fluxo de Carregamento

```
Digite o ID do seu personagem: [Número do ID]
```

## 🎮 Comandos Durante o Jogo

### Comandos Principais

| Comando | Descrição | Sintaxe | Exemplo |
|---------|-----------|---------|---------|
| `status` | Mostra informações do personagem | `status` | `status` |
| `viajar` | Inicia sistema de viagem | `viajar` | `viajar` |
| `missoes` | Lista missões disponíveis | `missoes` | `missoes` |
| `sair` | Volta ao menu principal | `sair` | `sair` |

### Comando: `status`

**Função**: Exibe informações detalhadas do personagem atual

**Saída Esperada**:
```
=== Status do Personagem ===
Classe: Jedi
Planeta atual: Tatooine
Level: 1
Vida: 100
GCS: 1000
```

**Informações Mostradas**:
- **Classe**: Jedi, Sith ou Caçador de Recompensas
- **Planeta atual**: Localização atual do personagem
- **Level**: Nível atual (1-100)
- **Vida**: Pontos de vida atuais
- **GCS**: Créditos galácticos disponíveis

### Comando: `viajar`

**Função**: Sistema completo de viagem entre planetas

**Fluxo do Comando**:

1. **Lista de Naves Disponíveis**:
```
=== Suas Naves ===
Modelo          | Tipo            | Velocidade | Capacidade
------------------------------------------------------------
1. YT-1300-001   | YT-1300        | 145        | 5
```

2. **Localização Atual e Destinos**:
```
Você está em: Tatooine

Planetas disponíveis:
- Coruscant | Clima: Temperado (Requer nave com velocidade 150)
- Naboo | Clima: Temperado (Sem requisitos)
- Kashyyyk | Clima: Tropical (Sem requisitos)
- Hoth | Clima: Gelado (Sem requisitos)
```

3. **Seleção de Destino**:
```
Para qual planeta deseja viajar? [Digite o nome do planeta]
```

4. **Seleção de Nave**:
```
Escolha o número da nave (1 para YT-1300 padrão): [Digite o número]
```

**Validações Automáticas**:
- ✅ Verificação de propriedade da nave
- ✅ Validação de velocidade mínima
- ✅ Confirmação de destino válido

**Mensagens de Sucesso**:
```
Viagem concluída! Você chegou em Naboo usando YT-1300-001
```

**Mensagens de Erro**:
```
Você não possui esta nave!
Sua nave é muito lenta para viajar para Coruscant!
Velocidade mínima necessária: 150
Velocidade da sua nave: 145
```

### Comando: `missoes`

**Função**: Lista missões disponíveis (em desenvolvimento)

**Status Atual**: Comando reconhecido mas funcionalidade não implementada

**Implementação Futura**:
```
=== Missões Disponíveis ===
1. [Entrega] Transportar suprimentos para Hoth
   Recompensa: 500 GCS, 200 XP
   
2. [Eliminação] Derrotar piratas em Tatooine
   Recompensa: 750 GCS, 300 XP
```

### Comando: `sair`

**Função**: Retorna ao menu principal

**Comportamento**:
- Salva automaticamente o progresso
- Limpa a sessão atual
- Retorna ao menu de seleção de personagem

## 🔧 Comandos de Sistema

### Tratamento de Erros

| Situação | Comando Digitado | Resposta do Sistema |
|----------|------------------|-------------------|
| Comando inválido | `xyz` | Comando não reconhecido |
| Classe inexistente | `Padawan` | Erro ao criar personagem: foreign key constraint |
| Planeta inexistente | `Alderaan` | Planeta não encontrado |
| ID inválido | `abc` | Personagem não encontrado |

### Comandos Case-Insensitive

**Comandos que aceitam variações**:
- `STATUS` = `status` = `Status`
- `VIAJAR` = `viajar` = `Viajar`
- `SAIR` = `sair` = `Sair`

**Nomes que devem ser exatos**:
- Classes: `Jedi`, `Sith`, `Cacador_de_Recompensas`
- Planetas: `Tatooine`, `Coruscant`, `Naboo`, `Kashyyyk`, `Hoth`

## 📝 Convenções de Entrada

### Formatação de Comandos
- **Comandos simples**: Digite exatamente como mostrado
- **Parâmetros**: Substitua `<parâmetro>` pelo valor desejado
- **Opcionais**: Parâmetros entre `[colchetes]` são opcionais

### Caracteres Especiais
- **Espaços**: Permitidos em nomes de planetas
- **Underscores**: Necessários em `Cacador_de_Recompensas`
- **Números**: Aceitos para seleção de naves e opções

### Validação de Entrada
- **Timeout**: Comandos não expiram (aguarda entrada)
- **Cancelamento**: Use `Ctrl+C` para interromper
- **Histórico**: Não implementado (use setas do terminal)

## 🔍 Debugging e Logs

### Informações de Debug
- **Conexão**: Status da conexão com banco
- **Transações**: Confirmação de operações
- **Erros**: Mensagens detalhadas de erro

### Logs do Sistema
```
Iniciando aplicação Star Wars MUD...
Conexão com o banco de dados estabelecida!
Personagem criado com sucesso! ID: 1
Viagem concluída! Você chegou em Naboo usando YT-1300-001
```

---

## 💡 Dicas de Uso

1. **Comandos são case-insensitive** para ações, mas case-sensitive para nomes
2. **Use Tab** para autocompletar (não implementado ainda)
3. **Ctrl+C** interrompe o jogo a qualquer momento
4. **IDs de personagem** são únicos e incrementais
5. **Nomes exatos** são necessários para classes e planetas

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento de comandos do MUD          | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |
