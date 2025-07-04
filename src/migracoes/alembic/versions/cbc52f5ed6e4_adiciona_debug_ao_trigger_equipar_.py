"""Adiciona debug ao trigger equipar_jogador

Revision ID: [ID GERADO AUTOMATICAMENTE]
Revises: 002 # <-- Coloque aqui o ID da sua última migração, ex: 'zzzzzzzz'
Create Date: 2025-06-30 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '[ID GERADO AUTOMATICAMENTE]'
down_revision = '002' # <-- Coloque aqui o ID da sua última migração
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION equipar_jogador()
        RETURNS TRIGGER AS $$
        DECLARE
            novo_modelo_nave VARCHAR(30);
        BEGIN
            RAISE NOTICE '[DEBUG] TRIGGER DISPARADO para o Personagem ID: %', NEW.id_player;

            -- cria inventario novo do jogador
            INSERT INTO Inventario (Id_PlayerIn, Id_Player, Espaco_Maximo, Peso_Total)
            VALUES (NEW.id_player, NEW.id_player, 20, 0);
            RAISE NOTICE '[DEBUG] Inventario inserido com sucesso.';

            -- gera um modelo único para a nave YT-1300 do jogador
            novo_modelo_nave := 'YT-1300-' || LPAD(NEW.id_player::TEXT, 3, '0');
            RAISE NOTICE '[DEBUG] Modelo de nave gerado: %', novo_modelo_nave;

            -- cria uma nova nave YT-1300 para o jogador
            INSERT INTO Nave (modelo, Id_Player, velocidade, capacidade)
            VALUES (novo_modelo_nave, NEW.id_player, 145, 5);
            RAISE NOTICE '[DEBUG] Nave inserida com sucesso.';

            -- registra a nave na tabela específica YT_1300
            INSERT INTO YT_1300 (modelo)
            VALUES (novo_modelo_nave);
            RAISE NOTICE '[DEBUG] YT-1300 inserido com sucesso.';

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    # Opcional: Aqui você pode colocar o código original da função para reverter
    pass
