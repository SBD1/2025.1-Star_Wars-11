"""Popular mais inimigos seguindo lógica de nível de perigo

Revision ID: 032
Revises: 031
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '032'
down_revision = '031'
branch_labels = None
depends_on = None

def upgrade():

    op.execute("""
        -- Criando tabela de Missão Mobs
        CREATE TABLE Missao_Mobs (
        id_mob INT NOT NULL,
        id_missao INT NOT NULL,
        tipo_mob VARCHAR(22) NOT NULL,
        planeta_origem VARCHAR(20) NOT NULL,
        setor VARCHAR(20) NOT NULL,
        xp_recompensa INT NOT NULL DEFAULT 0,
        creditos_recompensa INT NOT NULL DEFAULT 0,
        nivel_minimo INT NOT NULL DEFAULT 1,
        ativa BOOLEAN NOT NULL DEFAULT true,
        FOREIGN KEY (id_mob) REFERENCES Inimigo(id_mob),
        FOREIGN KEY (id_missao) REFERENCES Missao(id_missao)

    );
    """)
    op.execute("""
        -- Inserindo coluna na tabela Inimigo 
        ALTER TABLE Inimigo 
        ADD COLUMN
        vida_atual INT NOT NULL DEFAULT 100;
               
""")
    
def downgrade():

    op.execute("""
        -- Remover tabela Missao_Mobs
        DROP TABLE IF EXISTS Missao_Mobs;
    """)

    op.execute("""
        -- Remover coluna vida_atual da tabela Inimigo
        ALTER TABLE Inimigo
        DROP COLUMN vida_atual;
    """)
