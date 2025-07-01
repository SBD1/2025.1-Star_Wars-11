"""Adicionar stored procedures

Revision ID: 003
Revises: 002
Create Date: 2025-01-20 10:00:00.000000

"""
import os
from alembic import op

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade():
    """Adiciona as stored procedures reorganizadas ao banco de dados"""

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL', 'procedures')
    )

    # Lista de arquivos de procedures organizados por módulo
    arquivos_procedures = [
        'personagem_procedures.sql',
        'inventario_procedures.sql',
        'loja_procedures.sql',
        'combate_procedures.sql',
        'missao_procedures.sql',
        'admin_procedures.sql',
    ]

    for nome_arquivo in arquivos_procedures:
        caminho_arquivo = os.path.join(base_dir, nome_arquivo)

        if not os.path.isfile(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

        print(f"Executando procedures de: {nome_arquivo}")

        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            op.execute(conteudo)

        print(f"✅ Procedures de {nome_arquivo} executadas com sucesso")

def downgrade():
    """Remove as stored procedures reorganizadas do banco de dados"""

    procedures_para_remover = [
        # Admin
        'backup_stats', 'limpar_dados_teste', 'analise_economia', 'top_jogadores',
        'atividade_planetas', 'relatorio_servidor',
        # Missões
        'missoes_planeta', 'progresso_missoes', 'missoes_disponiveis', 'minhas_missoes',
        'abandonar_missao', 'aceitar_missao',
        # Combate
        'simular_combate', 'inimigos_planeta', 'calcular_dano', 'iniciar_combate',
        # Loja
        'historico_transacoes', 'poder_compra', 'consultar_loja', 'vender_item', 'comprar_item',
        # Inventário
        'consultar_inventario', 'trocar_itens', 'remover_item', 'adicionar_item',
        # Personagem
        'ranking_poder', 'status_personagem', 'subir_level', 'novo_personagem',
    ]

    for nome_procedure in procedures_para_remover:
        try:
            op.execute(f"DROP FUNCTION IF EXISTS {nome_procedure} CASCADE;")
            print(f"✅ Procedure {nome_procedure} removida")
        except Exception as e:
            print(f"⚠️  Erro ao remover {nome_procedure}: {e}")

    print("🗑️  Downgrade das procedures reorganizadas concluído")
