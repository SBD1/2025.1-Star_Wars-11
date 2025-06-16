import os
from alembic import op

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade():
    base_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DML')
    )
    arquivos = [
        'dml_sistema_planeta.sql',
        'dml_personagem.sql',
        'dml_classes_especializadas.sql',
        'dml_npcs.sql',
        'dml_missao.sql',
        'dml_nave.sql',
        'dml_mobs.sql',
        'dml_inventario_jogador.sql',
    ]
    for nome in arquivos:
        caminho = os.path.join(base_dir, nome)
        with open(caminho, 'r', encoding='utf-8') as f:
            op.execute(f.read())

def downgrade():
    pass
