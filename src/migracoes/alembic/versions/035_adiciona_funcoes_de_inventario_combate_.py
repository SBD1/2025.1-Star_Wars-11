"""Adiciona funcoes de inventario, combate e sistema de loot

Revision ID: cfeeefe37d20
Revises: 034
Create Date: 2025-07-07 14:31:42.117379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfeeefe37d20'
down_revision: Union[str, None] = '034'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sql_commands = """
    CREATE OR REPLACE FUNCTION adicionar_item_inventario( 
         jogador_id INT,  
         item_id_add INT,  
         quantidade_add INT 
     ) 
     RETURNS TEXT AS $$ 
     DECLARE 
         inventario_id INT; 
         item_existente INT; 
     BEGIN 
         SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = jogador_id; 
         IF NOT FOUND THEN RETURN 'Erro: Inventário do jogador não encontrado.'; END IF; 
         SELECT quantidade INTO item_existente FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_add; 
         IF FOUND THEN 
             UPDATE Inventario_Item SET quantidade = quantidade + quantidade_add WHERE Id_PlayerIn = inventario_id AND id_item = item_id_add; 
         ELSE 
             INSERT INTO Inventario_Item (Id_PlayerIn, id_item, quantidade) VALUES (inventario_id, item_id_add, quantidade_add); 
         END IF; 
         RETURN (SELECT nome FROM Item WHERE id_item = item_id_add) || ' (x' || quantidade_add || ') adicionado ao inventário.'; 
     END; 
     $$ LANGUAGE plpgsql; 

     CREATE OR REPLACE FUNCTION listar_inventario_jogador(jogador_id INT) 
     RETURNS TABLE ( 
         id_item INT, nome_item VARCHAR(50), quantidade INT, tipo_item VARCHAR(20), peso_item INT 
     ) AS $$ 
     BEGIN 
         RETURN QUERY 
         SELECT i.id_item, i.nome, ii.quantidade, i.tipo, i.Peso 
         FROM Inventario inv 
         JOIN Inventario_Item ii ON inv.Id_PlayerIn = ii.Id_PlayerIn 
         JOIN Item i ON ii.id_item = i.id_item 
         WHERE inv.Id_Player = jogador_id 
         ORDER BY i.nome; 
     END; 
     $$ LANGUAGE plpgsql; 

     CREATE OR REPLACE FUNCTION usar_item_inventario( 
         jogador_id INT,  
         item_id_usar INT 
     ) 
     RETURNS TEXT AS $$ 
     DECLARE 
         inventario_id INT; 
         item_info RECORD; 
         quantidade_atual INT; 
         vida_maxima INT; 
     BEGIN 
         SELECT Id_PlayerIn INTO inventario_id FROM Inventario WHERE Id_Player = jogador_id; 
         SELECT quantidade INTO quantidade_atual FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar; 
         IF NOT FOUND OR quantidade_atual <= 0 THEN 
             RETURN 'Você não possui este item.'; 
         END IF; 

         SELECT nome, efeito_tipo, efeito_valor INTO item_info FROM Item WHERE id_item = item_id_usar; 

         CASE item_info.efeito_tipo 
             WHEN 'CURA_VIDA' THEN 
                 SELECT vida_base INTO vida_maxima FROM Personagem WHERE id_player = jogador_id; 
                 UPDATE Personagem 
                 SET vida_atual = LEAST(vida_maxima, vida_atual + item_info.efeito_valor) 
                 WHERE id_player = jogador_id; 
             ELSE 
                 RETURN 'Este item não pode ser usado.'; 
         END CASE; 

         IF quantidade_atual > 1 THEN 
             UPDATE Inventario_Item SET quantidade = quantidade - 1 WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar; 
         ELSE 
             DELETE FROM Inventario_Item WHERE Id_PlayerIn = inventario_id AND id_item = item_id_usar; 
         END IF; 
          
         RETURN 'Você usou ' || item_info.nome || '. Sua vida foi restaurada!'; 
     END; 
     $$ LANGUAGE plpgsql; 

     CREATE OR REPLACE FUNCTION administrar_adicionar_item( 
         p_player_id INT, 
         p_item_name TEXT, 
         p_quantity INT 
     ) 
     RETURNS TEXT AS $$ 
     DECLARE 
         v_item_id INT; 
         v_result_text TEXT; 
     BEGIN 
         SELECT id_item INTO v_item_id FROM Item WHERE nome = p_item_name; 
         IF NOT FOUND THEN 
             RETURN 'ERRO: Item com o nome "' || p_item_name || '" não foi encontrado.'; 
         END IF; 
         SELECT adicionar_item_inventario(p_player_id, v_item_id, p_quantity) INTO v_result_text; 
         RETURN v_result_text; 
     END; 
     $$ LANGUAGE plpgsql; 

     CREATE OR REPLACE FUNCTION listar_inimigos_planeta(jogador_id INT) 
     RETURNS TABLE ( 
         id_mob INT, 
         tipo_mob VARCHAR(22), 
         vida_base INT, 
         nivel INT, 
         dano_base INT, 
         pontos_escudo INT, 
         creditos INT, 
         nivel_ameaca INT 
     ) AS $$ 
     BEGIN 
         RETURN QUERY 
         SELECT  
             i.id_mob, 
             i.tipo_mob, 
             i.vida_base, 
             i.nivel, 
             i.dano_base, 
             i.pontos_escudo, 
             i.creditos, 
             m.nivel_ameaca 
         FROM Inimigo i 
         JOIN MOB m ON i.tipo_mob = m.tipo_mob 
         JOIN Personagem p ON p.nome_planeta = i.planeta_origem 
         WHERE p.id_player = jogador_id 
         ORDER BY m.nivel_ameaca, i.nivel; 
     END; 
     $$ LANGUAGE plpgsql; 
     
     CREATE OR REPLACE FUNCTION finalizar_combate(combate_id INT, vencedor VARCHAR(10)) 
     RETURNS TEXT AS $$ 
     DECLARE 
         jogador_id INT; 
         inimigo_id INT; 
         jogador_level_atual INT; 
         novo_level INT; 
         xp_recompensa INT; 
         gcs_recompensa INT; 
         nivel_inimigo INT; 
         creditos_inimigo INT; 
         resultado_texto TEXT; 
         data_inicio_combate TIMESTAMP; 
         duracao INTERVAL; 
         total_turnos INT; 
         dano_total_jogador INT; 
         dano_total_inimigo INT; 
         vida_ressurreicao INT; 
         gcs_atual INT; 
         loot_drop RECORD; 
         drop_chance NUMERIC; 
         chance_roll NUMERIC; 
         loot_texto TEXT := ''; 
     BEGIN 
         SELECT id_player, id_mob, data_inicio INTO jogador_id, inimigo_id, data_inicio_combate 
         FROM Combate WHERE id_combate = combate_id; 

         IF NOT FOUND THEN 
             RETURN 'Erro: Combate nao encontrado'; 
         END IF; 

         duracao := CURRENT_TIMESTAMP - data_inicio_combate; 

         SELECT COUNT(*), 
                COALESCE(SUM(CASE WHEN ator = 'jogador' THEN dano_causado ELSE 0 END), 0), 
                COALESCE(SUM(CASE WHEN ator = 'inimigo' THEN dano_causado ELSE 0 END), 0) 
         INTO total_turnos, dano_total_jogador, dano_total_inimigo 
         FROM Combate_Log WHERE id_combate = combate_id; 

         IF vencedor = 'jogador' THEN 
             SELECT nivel, creditos INTO nivel_inimigo, creditos_inimigo 
             FROM Inimigo WHERE id_mob = inimigo_id; 
             xp_recompensa := nivel_inimigo * 50 + 25; 
             gcs_recompensa := creditos_inimigo; 
             SELECT level INTO jogador_level_atual FROM Personagem WHERE id_player = jogador_id; 
             novo_level := LEAST(floor((xp_recompensa + (SELECT xp FROM Personagem WHERE id_player = jogador_id)) / 100.0) + 1, 50); 

             UPDATE Personagem 
             SET xp = xp + xp_recompensa, 
                 gcs = gcs + gcs_recompensa, 
                 level = novo_level, 
                 vitorias = vitorias + 1, 
                 vida_base = 100
             WHERE id_player = jogador_id; 

             FOR loot_drop IN  
                 SELECT * FROM Inventario_IA WHERE id_mob = inimigo_id 
             LOOP 
                 drop_chance := CASE loot_drop.drop_rarity 
                                     WHEN 'Comum' THEN 60.0 
                                     WHEN 'Incomum' THEN 25.0 
                                     WHEN 'Raro' THEN 5.0 
                                     WHEN 'Épico' THEN 1.0 
                                     WHEN 'Garantido' THEN 100.0 
                                     ELSE 0.0 
                                END; 
                 chance_roll := random() * 100;
                 IF chance_roll < drop_chance THEN 
                     PERFORM adicionar_item_inventario(jogador_id, loot_drop.id_item, loot_drop.quantidade); 
                     loot_texto := loot_texto || ' | Loot: ' || (SELECT nome FROM Item WHERE id_item = loot_drop.id_item) || ' (x' || loot_drop.quantidade || ')'; 
                 END IF; 
             END LOOP; 

             resultado_texto := 'Vitoria! Voce ganhou ' || xp_recompensa || ' XP e ' || gcs_recompensa || ' GCS.' || loot_texto; 

             IF novo_level > jogador_level_atual THEN 
                 resultado_texto := resultado_texto || ' Parabens! Voce subiu para o level ' || novo_level || '!'; 
             END IF; 

         ELSIF vencedor = 'inimigo' THEN 
             SELECT level, gcs INTO jogador_level_atual, gcs_atual FROM Personagem WHERE id_player = jogador_id; 

             IF gcs_atual >= 100 THEN 
                 vida_ressurreicao := 100;
             ELSE 
                 vida_ressurreicao := 50;
             END IF; 

             UPDATE Personagem 
             SET mortes = mortes + 1, 
                 gcs = GREATEST(gcs - 100, 0),
                 xp = GREATEST(xp - (level * 10), 0),
                 vida_base = vida_ressurreicao
             WHERE id_player = jogador_id; 

             IF gcs_atual >= 100 THEN 
                 resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu 100 GCS e ' || (jogador_level_atual * 10) || ' XP. Ressuscitou com vida completa.'; 
             ELSE 
                 resultado_texto := 'Derrota! Voce foi derrotado em combate. Perdeu ' || gcs_atual || ' GCS e ' || (jogador_level_atual * 10) || ' XP. Sem dinheiro suficiente - ressuscitou com vida reduzida (50 HP).'; 
             END IF; 
         ELSE 
             UPDATE Personagem 
             SET vida_base = 100 
             WHERE id_player = jogador_id; 
             resultado_texto := 'Voce fugiu do combate.'; 
         END IF; 

         UPDATE Combate 
         SET status_combate = CASE 
                                 WHEN vencedor = 'jogador' THEN 'vitoria' 
                                 WHEN vencedor = 'inimigo' THEN 'derrota' 
                                 ELSE 'fugiu' 
                             END, 
             data_fim = CURRENT_TIMESTAMP 
         WHERE id_combate = combate_id; 

         RETURN resultado_texto; 
     END; 
     $$ LANGUAGE plpgsql;
    """
    op.execute(sql_commands)
    pass
