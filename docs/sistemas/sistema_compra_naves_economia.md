# Sistema de Compra de Naves e Economia Melhorada

## Visão Geral

Este sistema implementa uma economia robusta para o jogo Star Wars MUD, incluindo:

- **Loja de Naves**: Sistema completo de compra e venda de naves
- **Drops Melhorados**: Mobs dropam mais dinheiro (Normal 2x, Elite 3x, Boss 5x)
- **Respawn Automático**: Sistema de respawn de mobs via triggers e cron jobs
- **Sistema de Cron**: Jobs automáticos para manutenção do sistema

## 🚀 Sistema de Loja de Naves

### Tabelas Criadas

- **`Loja_Nave`**: Catálogo de naves disponíveis para compra
- **`Sistema_Log`**: Log de todas as transações e eventos

### Naves Disponíveis

| Nave | Preço | Velocidade | Capacidade | Nível Min | Local |
|------|-------|------------|------------|-----------|-------|
| X-Wing T-65 Caça Estelar | 15,000 GCS | 170 | 1 | 3 | Tatooine |
| YT-1300 Cargueiro | 25,000 GCS | 145 | 5 | 1 | Tatooine |
| Lambda Shuttle Imperial | 45,000 GCS | 160 | 20 | 8 | Coruscant |
| X-Wing T-65 Elite | 35,000 GCS | 180 | 1 | 10 | Coruscant |
| Fregata Corelliana CR90 | 150,000 GCS | 180 | 100 | 15 | Kashyyyk |
| Millennium Falcon Replica | 80,000 GCS | 165 | 8 | 12 | Kashyyyk |

### Funções Disponíveis

#### Listar Naves Disponíveis
```sql
SELECT * FROM listar_naves_disponiveis(jogador_id);
```

#### Comprar Nave
```sql
SELECT comprar_nave(jogador_id, id_loja_nave);
```

#### Vender Nave
```sql
SELECT vender_nave(jogador_id, 'modelo_da_nave');
```

## 💰 Sistema de Drops Melhorado

### Multiplicadores de Créditos

- **Mobs Normais**: 2x créditos originais
- **Mobs Elite**: 3x créditos originais  
- **Mobs Boss**: 5x créditos originais

### Sistema de Drop Variável

- Cada mob dropa ±25% do valor base
- Função: `calcular_drop_creditos(id_inimigo)`
- Garante mínimo de 1 crédito por kill

### Exemplos de Drops

| Tipo | Mob | Créditos Base | Drop Variável |
|------|-----|---------------|---------------|
| Normal | Stormtrooper | 100 | 75-125 |
| Elite | Dark Trooper | 450 | 337-562 |
| Boss | Rancor | 2,500 | 1,875-3,125 |

## 🔄 Sistema de Respawn Automático

### Tabelas de Controle

- **`Mob_Respawn_Control`**: Controla respawn individual de cada mob
- **`Sistema_Cron_Jobs`**: Gerencia jobs automáticos

### Mecânica de Respawn

1. **Morte do Mob**: Trigger reduz `quantidade_atual` 
2. **Timer de Respawn**: Baseado em `taxa_respawn` da tabela `Inimigo_Setor`
3. **Respawn Automático**: Cron job executa a cada 30 segundos
4. **Limite Máximo**: Respeitado por `quantidade_maxima`

### Intervalos de Respawn por Tipo

- **Mobs Normais**: 120-300 segundos
- **Mobs Elite**: 300-600 segundos  
- **Mobs Boss**: 600-1800 segundos

## ⚙️ Sistema de Cron Jobs

### Jobs Automáticos

1. **`respawn_mobs`**: Processa respawn (30s)
2. **`limpeza_logs`**: Remove logs antigos (1h)
3. **`backup_economia`**: Snapshot econômico (30min)

### Triggers Automáticos

- **Combate Finalizado**: Executa cron após cada combate
- **Controle de Frequência**: Evita execução excessiva (25s mínimo)

### Funções de Controle

#### Executar Cron Manualmente
```sql
SELECT executar_cron_manual();
```

#### Verificar Status do Sistema
```sql
SELECT * FROM status_sistema_cron();
```

#### Forçar Respawn de Mobs
```sql
SELECT processar_respawn_mobs();
```

## 📊 Monitoramento e Logs

### Eventos Logados

- `compra_nave`: Compras de naves
- `venda_nave`: Vendas de naves
- `mob_respawn`: Respawn de mobs
- `cron_job_sucesso`: Execução bem-sucedida de jobs
- `cron_job_erro`: Erros em jobs
- `backup_economia`: Snapshots econômicos

### Consultas Úteis

#### Ver Logs Recentes
```sql
SELECT * FROM Sistema_Log 
WHERE timestamp_evento > CURRENT_TIMESTAMP - INTERVAL '1 hour'
ORDER BY timestamp_evento DESC;
```

#### Estatísticas de Respawn
```sql
SELECT 
    i.tipo_mob,
    COUNT(*) as total_spawns,
    AVG(mrc.quantidade_atual) as media_quantidade
FROM Mob_Respawn_Control mrc
JOIN Inimigo_Setor ies ON mrc.id_inimigo_setor = ies.id_inimigo_setor
JOIN Inimigo i ON ies.id_mob = i.id_mob
GROUP BY i.tipo_mob;
```

#### Economia do Servidor
```sql
SELECT 
    SUM(gcs) as total_gcs_circulacao,
    AVG(gcs) as media_gcs_jogador,
    COUNT(*) as total_jogadores
FROM Personagem;
```

## 🔧 Configuração e Manutenção

### Ajustar Intervalos de Respawn
```sql
UPDATE Sistema_Cron_Jobs 
SET intervalo_segundos = 60 
WHERE nome_job = 'respawn_mobs';
```

### Desativar/Ativar Jobs
```sql
UPDATE Sistema_Cron_Jobs 
SET ativo = false 
WHERE nome_job = 'backup_economia';
```

### Ajustar Preços de Naves
```sql
UPDATE Loja_Nave 
SET preco_gcs = 20000 
WHERE nome_comercial = 'X-Wing T-65 Caça Estelar';
```

### Limpar Logs Manualmente
```sql
SELECT limpar_logs_antigos();
```

## 🚨 Troubleshooting

### Problema: Mobs não estão respawnando
```sql
-- Verificar status do cron
SELECT * FROM status_sistema_cron();

-- Forçar execução
SELECT executar_cron_manual();

-- Verificar controles de respawn
SELECT * FROM Mob_Respawn_Control WHERE ativo = false;
```

### Problema: Economia inflacionada
```sql
-- Ver logs de transações
SELECT * FROM Sistema_Log WHERE evento IN ('compra_nave', 'venda_nave');

-- Ajustar drops de mobs
UPDATE Inimigo SET creditos = creditos * 0.8 WHERE tipo_mob IN (SELECT tipo_mob FROM Boss);
```

### Problema: Performance do sistema
```sql
-- Limpar logs antigos
SELECT limpar_logs_antigos();

-- Verificar jobs com erro
SELECT * FROM Sistema_Cron_Jobs WHERE contador_erros > 0;
```

## 📈 Balanceamento Econômico

### Valores Recomendados

- **GCS Inicial**: 1,000 (atual)
- **Drop Médio Normal**: 50-150 GCS
- **Drop Médio Elite**: 200-600 GCS  
- **Drop Médio Boss**: 1,000-5,000 GCS
- **Nave Básica**: 15,000-25,000 GCS
- **Nave Avançada**: 50,000-150,000 GCS

### Tempo para Comprar Naves

- **X-Wing Básico**: ~100-300 kills de mobs normais
- **Lambda Shuttle**: ~75-150 kills de mobs elite
- **Fregata CR90**: ~30-150 kills de mobs boss

Este sistema garante uma progressão econômica equilibrada e engajante para os jogadores!
