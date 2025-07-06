"""Corrigir tamanho do campo acao na tabela Combate_Log

Revision ID: 025
Revises: 024
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '025'
down_revision = '024'
branch_labels = None
depends_on = None

def upgrade():
    # Aumentar o tamanho do campo acao para suportar nomes de ataques especiais
    op.execute("""
        ALTER TABLE Combate_Log 
        ALTER COLUMN acao TYPE VARCHAR(50);
    """)

def downgrade():
    # Reverter para o tamanho original
    op.execute("""
        ALTER TABLE Combate_Log 
        ALTER COLUMN acao TYPE VARCHAR(20);
    """)
