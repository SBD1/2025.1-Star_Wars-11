"""add mercante tables and procedures

Revision ID: e51c33677dbc
Revises: 
Create Date: 2025-07-05 16:08:34.109725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e51c33677dbc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(open('src/DDL/ddl_mercante.sql').read())
    op.execute(open('src/DDL/ddl_mercante_procedures.sql').read())
    op.execute(open('src/DDL/ddl_mercante_triggers.sql').read())

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_check_inventario_mercante ON Inventario_Mercante;")
    op.execute("DROP FUNCTION IF EXISTS trg_check_inventario_mercante();")
    op.execute("DROP PROCEDURE IF EXISTS vender_item(INT, INT, INT, INT);")
    op.execute("DROP PROCEDURE IF EXISTS comprar_item(INT, INT, INT, INT);")
    op.execute("DROP TABLE IF EXISTS Inventario_Mercante;")
    op.execute("DROP TABLE IF EXISTS Mercante;")

