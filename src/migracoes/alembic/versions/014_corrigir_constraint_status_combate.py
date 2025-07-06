"""Corrigir constraint de status_combate para incluir vitoria e derrota

Revision ID: 014
Revises: 013
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '014'
down_revision = '013'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir a constraint de status_combate para incluir 'vitoria' e 'derrota'
    op.execute("""
        -- Remover a constraint antiga
        ALTER TABLE combate 
        DROP CONSTRAINT IF EXISTS combate_status_combate_check;
        
        -- Adicionar nova constraint com valores corretos
        ALTER TABLE combate 
        ADD CONSTRAINT combate_status_combate_check 
        CHECK (status_combate IN ('ativo', 'finalizado', 'fugiu', 'vitoria', 'derrota'));
    """)

def downgrade():
    # Reverter para a constraint original
    op.execute("""
        -- Remover a constraint nova
        ALTER TABLE combate 
        DROP CONSTRAINT IF EXISTS combate_status_combate_check;
        
        -- Adicionar constraint original (sem vitoria e derrota)
        ALTER TABLE combate 
        ADD CONSTRAINT combate_status_combate_check 
        CHECK (status_combate IN ('ativo', 'finalizado', 'fugiu'));
    """)
