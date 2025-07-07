"""add mercante tables and procedures

Revision ID: 9f7747214d2a
Revises: e51c33677dbc
Create Date: 2025-07-05 16:21:13.285691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f7747214d2a'
down_revision: Union[str, None] = 'e51c33677dbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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