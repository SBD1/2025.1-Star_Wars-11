"""Corrige localização inicial de novos personagens

Revision ID: e1f31201d7d1
Revises: 011
Create Date: 2025-07-05 22:14:41.482718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1f31201d7d1'
down_revision: Union[str, None] = '011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Atualiza trigger para colocar novos personagens no primeiro setor do planeta"""

    # Caminho para o arquivo de triggers
    import os
    ddl_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'DDL')
    )

    triggers_path = os.path.join(ddl_dir, 'ddl_triggers.sql')
    with open(triggers_path, 'r', encoding='utf-8') as f:
        triggers_content = f.read()

    op.execute(triggers_content)

    # Atualizar jogadores existentes que não têm localização
    op.execute("""
        UPDATE Personagem
        SET id_setor = (
            SELECT s.id_setor
            FROM Setor s
            JOIN Cidade c ON s.id_cidade = c.id_cidade
            WHERE c.nome_planeta = Personagem.nome_planeta
            ORDER BY s.nivel_perigo ASC, s.id_setor ASC
            LIMIT 1
        )
        WHERE id_setor IS NULL;
    """)

    print("✅ Trigger atualizado! Novos personagens serão automaticamente colocados no primeiro setor do planeta.")
    print("✅ Jogadores existentes sem localização foram atualizados.")


def downgrade() -> None:
    """Reverte o trigger para a versão anterior"""

    op.execute("""
        CREATE OR REPLACE FUNCTION equipar_jogador()
        RETURNS TRIGGER AS $$
        DECLARE
            novo_modelo_nave VARCHAR(30);
        BEGIN
            -- cria inventario novo do jogador
            INSERT INTO Inventario (Id_PlayerIn, Id_Player, Espaco_Maximo, Peso_Total)
            VALUES (NEW.id_player, NEW.id_player, 20, 0);

            -- gera um modelo único para a nave YT-1300 do jogador
            novo_modelo_nave := 'YT-1300-' || LPAD(NEW.id_player::TEXT, 3, '0');

            -- cria uma nova nave YT-1300 para o jogador
            INSERT INTO Nave (modelo, Id_Player, velocidade, capacidade)
            VALUES (novo_modelo_nave, NEW.id_player, 145, 5);

            -- registra a nave na tabela específica YT_1300
            INSERT INTO YT_1300 (modelo)
            VALUES (novo_modelo_nave);

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    print("Trigger revertido para versão anterior.")
