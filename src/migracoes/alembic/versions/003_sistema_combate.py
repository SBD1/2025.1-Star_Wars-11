"""Adiciona sistema de combate

Revision ID: 003
Revises: 002
Create Date: 2025-01-05 12:00:00.000000

"""
import os
from alembic import op

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    """Adiciona estruturas do sistema de combate"""
    
    # Caminho base para os arquivos DDL
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )
    
    # Lista de arquivos DDL para o sistema de combate
    arquivos_combate = [
        'ddl_combate.sql',
        'ddl_funcoes_combate.sql'
    ]
    
    # Executar cada arquivo DDL
    for nome_arquivo in arquivos_combate:
        caminho_arquivo = os.path.join(base_dir, nome_arquivo)
        
        if not os.path.isfile(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo DDL não encontrado: {caminho_arquivo}")
        
        print(f"Executando arquivo: {nome_arquivo}")
        
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            
            # Executar o conteúdo do arquivo
            op.execute(conteudo)
        
        print(f"Arquivo {nome_arquivo} executado com sucesso")
    
    print("Sistema de combate instalado com sucesso!")

def downgrade():
    """Remove estruturas do sistema de combate"""
    
    # Script para remover as tabelas e funções do sistema de combate
    op.execute("""
        -- Remover funções
        DROP FUNCTION IF EXISTS obter_status_combate(INT);
        DROP FUNCTION IF EXISTS finalizar_combate(INT, VARCHAR(10));
        DROP FUNCTION IF EXISTS processar_turno_inimigo(INT);
        DROP FUNCTION IF EXISTS processar_turno_jogador(INT, VARCHAR(20));
        DROP FUNCTION IF EXISTS calcular_dano(INT, BOOLEAN);
        DROP FUNCTION IF EXISTS iniciar_combate(INT, INT);
        DROP FUNCTION IF EXISTS listar_inimigos_planeta(INT);
        
        -- Remover tabelas (ordem inversa devido às foreign keys)
        DROP TABLE IF EXISTS Combate_Resultado CASCADE;
        DROP TABLE IF EXISTS Combate_Log CASCADE;
        DROP TABLE IF EXISTS Combate CASCADE;
        
        -- Remover índices (caso ainda existam)
        DROP INDEX IF EXISTS idx_combate_resultado_combate;
        DROP INDEX IF EXISTS idx_combate_log_combate;
        DROP INDEX IF EXISTS idx_combate_status;
        DROP INDEX IF EXISTS idx_combate_player;
    """)
    
    print("Sistema de combate removido com sucesso!")
