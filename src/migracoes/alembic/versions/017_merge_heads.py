"""Merge heads - unificar as duas linhas de migração

Revision ID: 017
Revises: 016, 1022b18909a3
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '017'
down_revision = ('016', '1022b18909a3')
branch_labels = None
depends_on = None

def upgrade():
    # Esta migração apenas unifica as duas heads, sem fazer alterações
    pass

def downgrade():
    # Não há downgrade necessário para uma migração de merge
    pass
