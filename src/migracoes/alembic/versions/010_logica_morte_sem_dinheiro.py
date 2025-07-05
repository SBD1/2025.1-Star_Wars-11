"""Adiciona lógica de morte sem dinheiro - volta com 50 de vida

Revision ID: 010
Revises: 009
Create Date: 2025-01-05 15:00:00.000000

"""
import os
from alembic import op

# revision identifiers, used by Alembic.
revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None

def upgrade():
    """Atualiza função finalizar_combate com lógica de morte sem dinheiro"""
    
    # Caminho para o arquivo de funções atualizado
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )
    
    arquivo_funcoes = os.path.join(base_dir, 'ddl_funcoes_combate.sql')
    
    if not os.path.isfile(arquivo_funcoes):
        raise FileNotFoundError(f"Arquivo DDL não encontrado: {arquivo_funcoes}")
    
    print("Atualizando função finalizar_combate com lógica de morte sem dinheiro...")
    
    with open(arquivo_funcoes, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
        
        # Executar o conteúdo do arquivo (vai recriar as funções)
        op.execute(conteudo)
    
    print("✅ Função atualizada!")
    print("📋 Nova lógica de morte:")
    print("   - Com ≥100 GCS: Perde 100 GCS, volta com 100 de vida")
    print("   - Com <100 GCS: Perde todos os GCS, volta com 50 de vida")

def downgrade():
    """Reverte as mudanças"""
    
    print("Revertendo lógica de morte sem dinheiro...")
    
    # Não há necessidade de reverter especificamente, 
    # pois a função anterior sempre dava 100 de vida
