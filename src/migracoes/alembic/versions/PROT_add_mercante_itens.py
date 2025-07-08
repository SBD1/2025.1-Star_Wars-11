# src/migracoes/versions/040_seed_mercante_products.py
"""seed mercante products

Revision ID: 040
Revises: 038
Create Date: 2025-07-08 22:45:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0412i912e0'
down_revision = '0e1ei12'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    -- Remove seed anterior (se existir)
    DELETE FROM Mercante_Produto 
     USING Mercante 
    WHERE Mercante_Produto.id_mercante = Mercante.id_mercante
      AND Mercante.nome = 'Mercado Coruscant';

    DELETE FROM Mercante 
     WHERE nome = 'Mercado Coruscant';

    -- Cria o mercante em Coruscant
    INSERT INTO Mercante (nome, nome_planeta)
    VALUES ('Mercado Coruscant', 'Coruscant');

    -- Popula o estoque com TODOS os itens existentes (os 6 do Item)
    INSERT INTO Mercante_Produto (id_mercante, id_item, preco, estoque)
    SELECT
      m.id_mercante,
      i.id_item,
      i.preco,
      5  -- estoque inicial fixo
    FROM Mercante m
    CROSS JOIN Item i
    WHERE m.nome = 'Mercado Coruscant';
    """)


def downgrade():
    op.execute("""
    DELETE FROM Mercante_Produto
     WHERE id_mercante = (
       SELECT id_mercante FROM Mercante WHERE nome = 'Mercado Coruscant'
     );

    DELETE FROM Mercante
     WHERE nome = 'Mercado Coruscant';
    """)
