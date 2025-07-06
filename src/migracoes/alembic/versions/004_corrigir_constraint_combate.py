"""Corrige constraint de ação no combate_log

Revision ID: 004
Revises: 003
Create Date: 2025-01-05 13:05:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None

def upgrade():
    """Corrige a constraint de ação para incluir 'inicio'"""
    
    # Remover a constraint antiga
    op.execute("""
        ALTER TABLE combate_log 
        DROP CONSTRAINT IF EXISTS combate_log_acao_check;
    """)
    
    # Adicionar a nova constraint com 'inicio'
    op.execute("""
        ALTER TABLE combate_log 
        ADD CONSTRAINT combate_log_acao_check 
        CHECK (acao IN ('ataque', 'defesa', 'fuga', 'habilidade', 'inicio'));
    """)
    
    print("Constraint de ação do combate_log corrigida com sucesso!")

def downgrade():
    """Reverte a constraint para o estado anterior"""
    
    # Remover a constraint nova
    op.execute("""
        ALTER TABLE combate_log 
        DROP CONSTRAINT IF EXISTS combate_log_acao_check;
    """)
    
    # Adicionar a constraint antiga sem 'inicio'
    op.execute("""
        ALTER TABLE combate_log 
        ADD CONSTRAINT combate_log_acao_check 
        CHECK (acao IN ('ataque', 'defesa', 'fuga', 'habilidade'));
    """)
    
    print("Constraint de ação do combate_log revertida!")
