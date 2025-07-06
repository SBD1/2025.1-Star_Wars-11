"""Corrige ambiguidade nas funções de combate

Revision ID: 005
Revises: 004
Create Date: 2025-01-05 13:10:00.000000

"""
import os
from alembic import op

# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None

def upgrade():
    """Atualiza as funções de combate com correções de ambiguidade"""
    
    # Caminho para o arquivo de funções corrigido
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )
    
    arquivo_funcoes = os.path.join(base_dir, 'ddl_funcoes_combate.sql')
    
    if not os.path.isfile(arquivo_funcoes):
        raise FileNotFoundError(f"Arquivo DDL não encontrado: {arquivo_funcoes}")
    
    print("Atualizando funções de combate...")
    
    with open(arquivo_funcoes, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
        
        # Executar o conteúdo do arquivo (vai recriar as funções)
        op.execute(conteudo)
    
    print("Funções de combate atualizadas com sucesso!")

def downgrade():
    """Remove as funções de combate"""
    
    op.execute("""
        -- Remover funções
        DROP FUNCTION IF EXISTS obter_status_combate(INT);
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        DROP FUNCTION IF EXISTS processar_turno_inimigo(INT);
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20));
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        DROP FUNCTION IF EXISTS iniciar_combate(INT, INT);
        DROP FUNCTION IF EXISTS listar_inimigos_planeta(INT);
    """)
    
    print("Funções de combate removidas!")
