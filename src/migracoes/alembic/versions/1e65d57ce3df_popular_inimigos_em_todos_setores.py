"""popular_inimigos_em_todos_setores

Revision ID: 1e65d57ce3df
Revises: e1f31201d7d1
Create Date: 2025-07-05 22:44:27.591881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e65d57ce3df'
down_revision: Union[str, None] = 'e1f31201d7d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Popular inimigos em todos os setores baseado no nível de perigo e planeta

    # CORUSCANT - Planeta Imperial (Dark Troopers e Stormtroopers)
    # Setores nível 1 (seguros) - poucos Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 2  -- 2 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Coruscant' AND s.nivel_perigo = 1;
    """)

    # Setores nível 2 (moderados) - mais Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 4  -- 4 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Coruscant' AND s.nivel_perigo = 2;
    """)

    # Setores nível 3+ (perigosos) - Dark Troopers + Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 3  -- 3 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Coruscant' AND s.nivel_perigo >= 3;
    """)

    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 2, 2  -- 2 Dark Troopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Coruscant' AND s.nivel_perigo >= 3;
    """)

    # TATOOINE - Planeta desértico (Stormtroopers e Rancors)
    # Setores nível 1 (seguros) - poucos Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 1  -- 1 Stormtrooper
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Tatooine' AND s.nivel_perigo = 1;
    """)

    # Setores nível 2 (moderados) - mais Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 3  -- 3 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Tatooine' AND s.nivel_perigo = 2;
    """)

    # Setores nível 3+ (perigosos) - Rancors + Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 2  -- 2 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Tatooine' AND s.nivel_perigo >= 3;
    """)

    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 3, 1  -- 1 Rancor
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Tatooine' AND s.nivel_perigo >= 3;
    """)

    # NABOO - Planeta pacífico (poucos inimigos, principalmente Stormtroopers)
    # Setores nível 1 (seguros) - muito poucos inimigos
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 1  -- 1 Stormtrooper
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Naboo' AND s.nivel_perigo = 1 AND s.tipo_setor NOT IN ('governamental');
    """)

    # Setores nível 2+ (moderados/perigosos) - alguns Stormtroopers
    op.execute("""
        INSERT INTO Inimigo_Setor (id_setor, id_mob, quantidade_maxima)
        SELECT s.id_setor, 1, 2  -- 2 Stormtroopers
        FROM Setor s
        JOIN Cidade c ON s.id_cidade = c.id_cidade
        WHERE c.nome_planeta = 'Naboo' AND s.nivel_perigo >= 2;
    """)


def downgrade() -> None:
    # Remover todos os inimigos dos setores
    op.execute("DELETE FROM Inimigo_Setor;")
