"""Corrigir constraint da tabela Combate_Log para incluir ataque_especial

Revision ID: 023
Revises: 022
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '023'
down_revision = '022'
branch_labels = None
depends_on = None

def upgrade():
    # Primeiro, atualizar registros problemáticos se existirem
    op.execute("""
        UPDATE Combate_Log
        SET acao = 'ataque'
        WHERE acao NOT IN ('ataque', 'defesa', 'fuga', 'ataque_especial');
    """)

    # Remover constraint antiga e adicionar nova que inclui ataque_especial
    op.execute("""
        ALTER TABLE Combate_Log
        DROP CONSTRAINT IF EXISTS combate_log_acao_check;

        ALTER TABLE Combate_Log
        ADD CONSTRAINT combate_log_acao_check
        CHECK (acao IN ('ataque', 'defesa', 'fuga', 'ataque_especial'));
    """)

def downgrade():
    # Reverter para constraint original
    op.execute("""
        ALTER TABLE Combate_Log 
        DROP CONSTRAINT IF EXISTS combate_log_acao_check;
        
        ALTER TABLE Combate_Log 
        ADD CONSTRAINT combate_log_acao_check 
        CHECK (acao IN ('ataque', 'defesa', 'fuga'));
    """)
