# Regras de Negócio - Star Wars MUD

## 📋 Visão Geral

Este documento define as regras de negócio que governam o funcionamento do Star Wars MUD, incluindo mecânicas de jogo, restrições e validações.

## 👤 Sistema de Personagens

### RN001 - Criação de Personagem
- **Regra**: Cada personagem deve ter uma classe válida e um planeta inicial
- **Validação**: Classe deve existir na tabela `Classe`
- **Validação**: Planeta deve existir na tabela `Planeta`
- **Implementação**: Foreign keys no banco de dados

### RN002 - Atributos Iniciais
- **Vida Base**: 100 pontos para todas as classes
- **Level Inicial**: 1 para todos os personagens
- **Dano Base**: 10 pontos para todas as classes
- **XP Inicial**: 0 pontos de experiência
- **GCS Inicial**: 1000 créditos galácticos

### RN003 - Identificação Única
- **Regra**: Cada personagem possui um ID único auto-incrementado
- **Implementação**: Campo `id_player` como chave primária

## 🌍 Sistema de Planetas

### RN004 - Planetas Disponíveis
- **Tatooine**: Planeta desértico, sem restrições de acesso
- **Coruscant**: Capital, requer nave com velocidade ≥ 150
- **Naboo**: Planeta pacífico, sem restrições
- **Kashyyyk**: Mundo dos Wookiees, sem restrições
- **Hoth**: Planeta gelado, sem restrições

### RN005 - Restrições de Viagem
- **Coruscant**: Velocidade mínima da nave = 150
- **Tatooine**: Velocidade mínima da nave = 100
- **Outros**: Sem restrições de velocidade

## 🚀 Sistema de Naves

### RN006 - Nave Padrão
- **Regra**: Todo personagem recebe uma YT-1300-001 ao ser criado
- **Especificações**: Velocidade 145, Capacidade 5
- **Implementação**: Inserção automática na tabela `Nave`

### RN007 - Propriedade de Naves
- **Regra**: Naves pertencem exclusivamente a um jogador
- **Validação**: Campo `Id_Player` deve corresponder ao dono
- **Restrição**: Jogador só pode usar suas próprias naves

### RN008 - Tipos de Naves
- **X-Wing T-65**: Caça estelar, velocidade 120, capacidade 1
- **YT-1300**: Cargueiro, velocidade 145, capacidade 5
- **Lambda Shuttle**: Transporte, velocidade 160, capacidade 20
- **Fregata CR90**: Nave capital, velocidade 180, capacidade 100

## 🎯 Sistema de Viagem

### RN009 - Validação de Viagem
1. **Verificar propriedade da nave**: Nave deve pertencer ao jogador
2. **Verificar velocidade**: Nave deve atender requisitos do destino
3. **Verificar destino**: Planeta deve existir e ser diferente do atual
4. **Atualizar localização**: Modificar `nome_planeta` do personagem

### RN010 - Custos de Viagem
- **Implementação Futura**: Sistema de combustível e custos
- **Atual**: Viagem gratuita para desenvolvimento

## 💰 Sistema Econômico

### RN011 - Moeda do Jogo
- **GCS**: Galactic Credit Standard (Crédito Galáctico Padrão)
- **Valor Inicial**: 1000 GCS por personagem
- **Uso**: Compra de itens, naves, serviços

### RN012 - Transações
- **Validação**: Saldo suficiente antes de qualquer compra
- **Atomicidade**: Transações devem ser completas ou revertidas
- **Auditoria**: Registro de todas as transações (implementação futura)

## ⚔️ Sistema de Combate (Futuro)

### RN013 - Cálculo de Dano
- **Fórmula Base**: `Dano = dano_base + modificadores_classe + modificadores_item`
- **Crítico**: 5% de chance de dano dobrado
- **Defesa**: Redução baseada em armaduras

### RN014 - Sistema de Vida
- **Morte**: Personagem com vida ≤ 0 deve ser revivido
- **Regeneração**: Vida regenera automaticamente fora de combate
- **Cura**: Itens e habilidades podem restaurar vida

## 🎮 Sistema de Progressão

### RN015 - Experiência (XP)
- **Ganho**: Completar missões, derrotar inimigos
- **Level Up**: A cada 1000 XP, level aumenta em 1
- **Benefícios**: Aumento de atributos por level

### RN016 - Limites de Level
- **Máximo**: Level 100
- **Progressão**: Exponencial (cada level requer mais XP)

## 🏆 Sistema de Missões (Futuro)

### RN017 - Tipos de Missão
- **Entrega**: Transportar itens entre planetas
- **Eliminação**: Derrotar inimigos específicos
- **Exploração**: Visitar locais específicos
- **Coleta**: Reunir recursos ou itens

### RN018 - Recompensas
- **XP**: Experiência baseada na dificuldade
- **GCS**: Créditos proporcionais ao esforço
- **Itens**: Equipamentos únicos ou raros

## 🔒 Validações de Integridade

### RN019 - Integridade Referencial
- **Personagem → Classe**: Deve existir classe válida
- **Personagem → Planeta**: Deve existir planeta válido
- **Nave → Personagem**: Deve pertencer a jogador existente
- **Missão → Planeta**: Deve estar em planeta válido

### RN020 - Validações de Dados
- **Vida**: Não pode ser negativa
- **Level**: Mínimo 1, máximo 100
- **GCS**: Não pode ser negativo
- **Velocidade**: Deve ser positiva

## 🔄 Regras de Atualização

### RN021 - Modificação de Personagem
- **Classe**: Não pode ser alterada após criação
- **Nome**: Pode ser alterado (implementação futura)
- **Atributos**: Apenas através de progressão ou itens

### RN022 - Exclusão de Dados
- **Personagem**: Pode ser deletado pelo próprio jogador
- **Cascata**: Exclusão remove naves e itens associados
- **Backup**: Dados são mantidos por 30 dias (implementação futura)

## 📊 Métricas e Balanceamento

### RN023 - Balanceamento de Classes
- **Jedi**: Equilibrado em ataque e defesa
- **Sith**: Alto dano, baixa defesa
- **Caçador**: Médio dano, alta precisão

### RN024 - Economia do Jogo
- **Inflação**: Controle de entrada de GCS no sistema
- **Sink**: Custos que removem GCS da economia
- **Balanceamento**: Ajustes baseados em métricas de uso

---

## 🔍 Implementação Técnica

### Triggers Necessários
- **Criação de Personagem**: Auto-inserir nave padrão
- **Level Up**: Atualizar atributos automaticamente
- **Validação de Viagem**: Verificar requisitos antes da viagem

### Procedures Necessárias
- **CalcularDano()**: Computar dano total em combate
- **ProcessarLevelUp()**: Gerenciar progressão de level
- **ValidarTransacao()**: Verificar saldo antes de compras

### Índices Recomendados
- **Personagem(nome_classe)**: Para consultas por classe
- **Nave(Id_Player)**: Para consultas de naves por jogador
- **Personagem(nome_planeta)**: Para consultas por localização

## Histórico de Versões

| Versão | Data       | Modificações                      | Autor(es)     | Revisor(es) |
|--------|------------|-----------------------------------|---------------|-------------|
| 1.0    | 16/06/2025 | Criação do documento de regras de negócios          | [Artur Mendonça](https://github.com/ArtyMend07) | [Amanda Abreu](https://github.com/Amandaaaaabreu) e [Eduardo Morais](https://github.com/Edumorais08) |