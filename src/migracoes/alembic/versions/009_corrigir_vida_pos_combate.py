"""Corrige atualização da vida do jogador após combate

Revision ID: 009
Revises: 008
Create Date: 2025-01-05 14:00:00.000000

"""
import os
from alembic import op

# revision identifiers, used by Alembic.
revision = '009'
down_revision = '008'
branch_labels = None
depends_on = None

def upgrade():
    """Atualiza função finalizar_combate para corrigir vida do jogador"""
    
    # Caminho para o arquivo de funções corrigido
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )
    
    arquivo_funcoes = os.path.join(base_dir, 'ddl_funcoes_combate.sql')
    
    if not os.path.isfile(arquivo_funcoes):
        raise FileNotFoundError(f"Arquivo DDL não encontrado: {arquivo_funcoes}")
    
    print("Atualizando função finalizar_combate para corrigir vida do jogador...")
    
    with open(arquivo_funcoes, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
        
        # Executar o conteúdo do arquivo (vai recriar as funções)
        op.execute(conteudo)
    
    print("Função finalizar_combate atualizada! Agora a vida do jogador é mantida após combate.")

def downgrade():
    """Reverte as mudanças"""
    
    print("Revertendo correção da vida pós-combate...")
    
    # Não há necessidade de reverter especificamente, 
    # pois a função anterior não atualizava a vida mesmo
