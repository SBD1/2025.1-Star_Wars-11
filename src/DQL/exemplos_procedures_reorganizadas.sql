-- EXEMPLOS DE USO DAS PROCEDURES REORGANIZADAS

-- Execute primeiro todos os arquivos de procedures:
-- \i src/DDL/procedures/personagem_procedures.sql
-- \i src/DDL/procedures/inventario_procedures.sql
-- \i src/DDL/procedures/loja_procedures.sql
-- \i src/DDL/procedures/combate_procedures.sql
-- \i src/DDL/procedures/missao_procedures.sql
-- \i src/DDL/procedures/admin_procedures.sql

-- ========================================
-- PERSONAGENS
-- ========================================

-- Criar personagens
SELECT novo_personagem('Jedi', 'Tatooine', 15) AS id_jedi;
SELECT novo_personagem('Sith', 'Coruscant', 12) AS id_sith;
SELECT novo_personagem('Cacador_de_Recompensas', 'Naboo', 18) AS id_cacador;

-- Ver status completo
SELECT * FROM status_personagem(1);

-- Ranking de poder
SELECT * FROM ranking_poder();

-- Forçar level up
SELECT subir_level(1);

-- ========================================
-- INVENTÁRIO
-- ========================================

-- Adicionar itens (certifique-se que existem itens cadastrados)
SELECT adicionar_item(1, 1, 3);
SELECT adicionar_item(1, 2, 1);

-- Consultar inventário
SELECT * FROM consultar_inventario(1);

-- Transferir entre jogadores
SELECT trocar_itens(1, 2, 1, 1);

-- Remover item
SELECT remover_item(1, 1, 1);

-- ========================================
-- LOJA
-- ========================================

-- Ver itens da loja
SELECT * FROM consultar_loja(1);

-- Ver poder de compra
SELECT * FROM poder_compra(1);

-- Comprar item
SELECT comprar_item(1, 1, 1, 2);

-- Vender item
SELECT vender_item(1, 1, 1, 1);

-- ========================================
-- COMBATE
-- ========================================

-- Ver inimigos do planeta
SELECT * FROM inimigos_planeta('Tatooine');

-- Combate simples
SELECT iniciar_combate(1, 1);

-- Combate detalhado
SELECT simular_combate(1, 1);

-- Calcular dano
SELECT calcular_dano(10, 5, 'critico');

-- ========================================
-- MISSÕES
-- ========================================

-- Ver missões disponíveis
SELECT * FROM missoes_disponiveis(1);

-- Aceitar missão
SELECT aceitar_missao(1, 1);

-- Ver minhas missões
SELECT * FROM minhas_missoes(1);

-- Progresso de missões
SELECT * FROM progresso_missoes(1);

-- Missões por planeta
SELECT * FROM missoes_planeta('Tatooine');

-- Abandonar missão
SELECT abandonar_missao(1, 1);

-- ========================================
-- ADMINISTRAÇÃO
-- ========================================

-- Relatório do servidor
SELECT * FROM relatorio_servidor();

-- Atividade por planeta
SELECT * FROM atividade_planetas();

-- Top jogadores
SELECT * FROM top_jogadores('poder');
SELECT * FROM top_jogadores('level');
SELECT * FROM top_jogadores('creditos');
SELECT * FROM top_jogadores('xp');

-- Análise econômica
SELECT * FROM analise_economia();

-- Backup de estatísticas
SELECT backup_stats();

-- ========================================
-- VERIFICAÇÕES ÚTEIS
-- ========================================

-- Verificar se as procedures foram criadas
SELECT proname, proargnames 
FROM pg_proc 
WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
AND proname IN ('novo_personagem', 'status_personagem', 'adicionar_item', 'iniciar_combate')
ORDER BY proname;

-- Ver dados básicos para testes
SELECT 'Personagens' AS tabela, COUNT(*) AS total FROM Personagem
UNION ALL
SELECT 'Itens', COUNT(*) FROM Item
UNION ALL
SELECT 'Inimigos', COUNT(*) FROM Inimigo
UNION ALL
SELECT 'Missões', COUNT(*) FROM Missao
UNION ALL
SELECT 'NPCs', COUNT(*) FROM Npc;

-- ========================================
-- LIMPEZA (CUIDADO!)
-- ========================================

-- Limpar dados de teste (descomente para usar)
-- SELECT limpar_dados_teste();
