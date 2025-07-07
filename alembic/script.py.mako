"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade():
    # Executa os scripts DDL de Mercante
    op.execute(open('src/DDL/ddl_mercante.sql', 'r').read())
    op.execute(open('src/DDL/ddl_mercante_procedures.sql', 'r').read())
    op.execute(open('src/DDL/ddl_mercante_triggers.sql', 'r').read())

def downgrade():
    # Desfaz as tabelas e triggers de Mercante
    op.execute("DROP TRIGGER IF EXISTS trg_check_inventario_mercante ON Inventario_Mercante;")
    op.execute("DROP FUNCTION IF EXISTS trg_check_inventario_mercante();")
    op.execute("DROP PROCEDURE IF EXISTS vender_item(INT, INT, INT, INT);")
    op.execute("DROP PROCEDURE IF EXISTS comprar_item(INT, INT, INT, INT);")
    op.execute("DROP TABLE IF EXISTS Inventario_Mercante;")
    op.execute("DROP TABLE IF EXISTS Mercante;")