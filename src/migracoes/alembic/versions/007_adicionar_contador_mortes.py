"""Adiciona contador de mortes e penalidades

Revision ID: 007
Revises: 006
Create Date: 2025-01-05 13:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007'
down_revision = '006'
branch_labels = None
depends_on = None

def upgrade():
    """Adiciona coluna de mortes e atualiza função de finalizar combate"""
    
    # Adicionar coluna de mortes na tabela Personagem
    op.add_column('personagem', sa.Column('mortes', sa.Integer(), nullable=False, server_default='0'))
    
    print("Coluna 'mortes' adicionada à tabela Personagem")

def downgrade():
    """Remove a coluna de mortes"""
    
    op.drop_column('personagem', 'mortes')
    
    print("Coluna 'mortes' removida da tabela Personagem")
