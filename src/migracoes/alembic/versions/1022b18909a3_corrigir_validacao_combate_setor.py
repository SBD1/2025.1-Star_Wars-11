"""corrigir_validacao_combate_setor

Revision ID: 1022b18909a3
Revises: 1e65d57ce3df
Create Date: 2025-07-05 23:06:18.671856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1022b18909a3'
down_revision: Union[str, None] = '1e65d57ce3df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Atualizar função iniciar_combate para usar validação baseada em setores
    op.execute("""
        -- Funcao para iniciar um combate (atualizada para sistema hierárquico)
        CREATE OR REPLACE FUNCTION iniciar_combate(jogador_id INT, inimigo_id INT)
        RETURNS TEXT AS $$
        DECLARE
            jogador_vida INT;
            inimigo_vida INT;
            jogador_setor INT;
            combate_id INT;
            inimigo_nome VARCHAR(22);
            inimigo_no_setor BOOLEAN := FALSE;
        BEGIN
            -- Verificar se o jogador existe e obter dados
            SELECT vida_base, id_setor INTO jogador_vida, jogador_setor
            FROM Personagem WHERE id_player = jogador_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Jogador nao encontrado';
            END IF;

            -- Verificar se o inimigo existe e obter dados
            SELECT vida_base, tipo_mob INTO inimigo_vida, inimigo_nome
            FROM Inimigo WHERE id_mob = inimigo_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Inimigo nao encontrado';
            END IF;

            -- Verificar se o inimigo esta no setor atual do jogador
            SELECT EXISTS(
                SELECT 1 FROM Inimigo_Setor
                WHERE id_setor = jogador_setor AND id_mob = inimigo_id AND ativo = true
            ) INTO inimigo_no_setor;

            IF NOT inimigo_no_setor THEN
                RETURN 'Erro: Voce nao pode lutar contra este inimigo. Ele nao esta no seu setor atual';
            END IF;

            -- Verificar se o jogador ja esta em combate
            SELECT id_combate INTO combate_id
            FROM Combate
            WHERE id_player = jogador_id AND status_combate = 'ativo';

            IF FOUND THEN
                RETURN 'Erro: Voce ja esta em combate. Finalize o combate atual primeiro';
            END IF;

            -- Criar novo combate
            INSERT INTO Combate (id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate)
            VALUES (jogador_id, inimigo_id, jogador_vida, inimigo_vida, 'ativo')
            RETURNING id_combate INTO combate_id;

            -- Registrar inicio do combate no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, 0, 'jogador', 'inicio', 0, jogador_vida, inimigo_vida,
                    'Combate iniciado contra ' || inimigo_nome);

            RETURN 'Combate iniciado contra ' || inimigo_nome || '! Use os comandos de combate para lutar.';
        END;
        $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    # Reverter para a função antiga baseada em planetas
    op.execute("""
        -- Funcao para iniciar um combate (versão antiga baseada em planetas)
        CREATE OR REPLACE FUNCTION iniciar_combate(jogador_id INT, inimigo_id INT)
        RETURNS TEXT AS $$
        DECLARE
            jogador_vida INT;
            inimigo_vida INT;
            inimigo_planeta VARCHAR(20);
            jogador_planeta VARCHAR(20);
            combate_id INT;
            inimigo_nome VARCHAR(22);
        BEGIN
            -- Verificar se o jogador existe e obter dados
            SELECT vida_base, nome_planeta INTO jogador_vida, jogador_planeta
            FROM Personagem WHERE id_player = jogador_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Jogador nao encontrado';
            END IF;

            -- Verificar se o inimigo existe e obter dados
            SELECT vida_base, planeta_origem, tipo_mob INTO inimigo_vida, inimigo_planeta, inimigo_nome
            FROM Inimigo WHERE id_mob = inimigo_id;

            IF NOT FOUND THEN
                RETURN 'Erro: Inimigo nao encontrado';
            END IF;

            -- Verificar se jogador e inimigo estao no mesmo planeta
            IF jogador_planeta != inimigo_planeta THEN
                RETURN 'Erro: Voce nao pode lutar contra este inimigo. Ele nao esta no seu planeta atual';
            END IF;

            -- Verificar se o jogador ja esta em combate
            SELECT id_combate INTO combate_id
            FROM Combate
            WHERE id_player = jogador_id AND status_combate = 'ativo';

            IF FOUND THEN
                RETURN 'Erro: Voce ja esta em combate. Finalize o combate atual primeiro';
            END IF;

            -- Criar novo combate
            INSERT INTO Combate (id_player, id_mob, vida_jogador_atual, vida_inimigo_atual, status_combate)
            VALUES (jogador_id, inimigo_id, jogador_vida, inimigo_vida, 'ativo')
            RETURNING id_combate INTO combate_id;

            -- Registrar inicio do combate no log
            INSERT INTO Combate_Log (id_combate, turno_numero, ator, acao, dano_causado,
                                    vida_restante_jogador, vida_restante_inimigo, descricao_acao)
            VALUES (combate_id, 0, 'jogador', 'inicio', 0, jogador_vida, inimigo_vida,
                    'Combate iniciado contra ' || inimigo_nome);

            RETURN 'Combate iniciado contra ' || inimigo_nome || '! Use os comandos de combate para lutar.';
        END;
        $$ LANGUAGE plpgsql;
    """)
