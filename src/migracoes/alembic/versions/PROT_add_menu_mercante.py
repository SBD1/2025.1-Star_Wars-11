# src/migracoes/versions/042_add_listar_acoes_mercante.py
"""add listar_acoes_jogo

Revision ID: 041
Revises: 040
Create Date: 2025-07-08 22:50:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0923jeu2m41'
down_revision = '04dm228d2mu0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE OR REPLACE FUNCTION listar_acoes_jogo(p_jogador_id INT)
    RETURNS TABLE(
        acao      VARCHAR,
        descricao VARCHAR
    ) AS $$
    BEGIN
        -- comandos sempre disponíveis
        RETURN QUERY
          SELECT 'status',     'status     - Ver status do personagem'
        UNION ALL SELECT 'viajar',     'viajar     - Viajar para outro planeta'
        UNION ALL SELECT 'missoes',    'missoes    - Sistema de missões'
        UNION ALL SELECT 'inventario', 'inventario - Abrir seu inventário';

        -- se houver mercante no planeta do personagem, adiciona comprar
        IF EXISTS(
          SELECT 1
            FROM Personagem p
            JOIN Mercante    m ON p.nome_planeta = m.nome_planeta
           WHERE p.id_player = p_jogador_id
        ) THEN
          RETURN QUERY
            SELECT 'comprar', 'comprar    - Comprar do mercante';
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade():
    op.execute("""
    DROP FUNCTION IF EXISTS listar_acoes_jogo(INT);
    """)