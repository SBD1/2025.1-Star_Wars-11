import os
from alembic import op

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():

    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )

    arquivos = [
        'ddl_sistema.sql',
        'ddl_planeta.sql',
        'ddl_personagem.sql',
        'ddl_npcs.sql',
        'ddl_missao.sql',
        'ddl_nave.sql',
        'ddl_mobs.sql',
        'ddl_triggers.sql',
        'ddl_inventario_jogador.sql',
    ]

    for nome in arquivos:
        caminho = os.path.join(base_dir, nome)
        if not os.path.isfile(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        with open(caminho, 'r', encoding='utf-8') as f:
            op.execute(f.read())

def downgrade():
    pass
