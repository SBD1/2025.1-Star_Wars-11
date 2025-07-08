# src/migracoes/versions/038_add_mercante_tables.py
"""add mercante tables

Revision ID: 038
Revises: 037
Create Date: 2025-07-07 22:00:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ewqweqwe'
down_revision = '123456'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    -- garante que não exista antes de criar
    DROP TABLE IF EXISTS Mercante_Produto;
    DROP TABLE IF EXISTS Mercante;

    -- cria tabela Mercante
    CREATE TABLE Mercante (
      id_mercante   SERIAL PRIMARY KEY,
      nome           VARCHAR(50) NOT NULL,
      nome_planeta   VARCHAR(50) NOT NULL
    );

    -- cria tabela Mercante_Produto referenciando Mercante e Item
    CREATE TABLE Mercante_Produto (
      id_mercante   INT NOT NULL,
      id_item       INT NOT NULL,
      preco         INT NOT NULL,
      estoque       INT NOT NULL DEFAULT 0,
      PRIMARY KEY (id_mercante, id_item),
      FOREIGN KEY (id_mercante) REFERENCES Mercante(id_mercante) ON DELETE CASCADE,
      FOREIGN KEY (id_item)       REFERENCES Item(id_item)      ON DELETE CASCADE
    );
    """)


def downgrade():
    op.execute("""
    DROP TABLE IF EXISTS Mercante_Produto;
    DROP TABLE IF EXISTS Mercante;
    """)
