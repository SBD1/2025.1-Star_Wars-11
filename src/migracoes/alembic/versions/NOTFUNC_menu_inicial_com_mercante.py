# src/migracoes/versions/043_universal_mercante.py
"""make merchant universal

Revision ID: 042
Revises: 041
Create Date: 2025-07-08 23:10:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '04198j3j8321j'
down_revision = '04m99nv4nnunu1'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CCREATE OR REPLACE FUNCTION listar_acoes_jogo(p_jogador_id INT)
RETURNS TABLE(acao VARCHAR, descricao VARCHAR) AS $$
BEGIN
  RETURN QUERY
    SELECT 'status',        'status          - Ver status do personagem'
  UNION ALL SELECT 'viajar',       'viajar          - Viajar para outro planeta'
  UNION ALL SELECT 'missoes',      'missoes         - Sistema de missões'
  UNION ALL SELECT 'inventario',   'inventario      - Abrir seu inventário'
  UNION ALL SELECT 'loja_de_itens','loja de itens   - Comprar do mercante';
END;
$$ LANGUAGE plpgsql;
    """)


def downgrade():
    op.execute("""
    -- volta ao comportamento anterior (com IF EXISTS)
    CREATE OR REPLACE FUNCTION listar_acoes_jogo(p_jogador_id INT)
    RETURNS TABLE(
        acao      VARCHAR,
        descricao VARCHAR
    ) AS $$
    BEGIN
        RETURN QUERY
          SELECT 'status',     'status     - Ver status do personagem'
        UNION ALL SELECT 'viajar',     'viajar     - Viajar para outro planeta'
        UNION ALL SELECT 'missoes',    'missoes    - Sistema de missões'
        UNION ALL SELECT 'inventario', 'inventario - Abrir seu inventário';

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
