"""Corrigir trigger mob_morto para usar estrutura correta da Combate_Resultado

Revision ID: 043
Revises: 042
Create Date: 2025-07-08

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '043'
down_revision = '042'
branch_labels = None
depends_on = None

def upgrade():
    # Corrigir o trigger que está causando erro ao acessar NEW.id_mob
    op.execute("""
        CREATE OR REPLACE FUNCTION trigger_mob_morto()
        RETURNS TRIGGER AS $$
        DECLARE
            inimigo_setor_id INT;
            inimigo_id INT;
        BEGIN
            -- Verificar se o combate foi vencido pelo jogador
            IF NEW.vencedor = 'jogador' THEN
                -- Obter o id_mob do combate relacionado
                SELECT c.id_mob INTO inimigo_id
                FROM Combate c
                WHERE c.id_combate = NEW.id_combate;
                
                IF inimigo_id IS NOT NULL THEN
                    -- Encontrar o inimigo_setor correspondente
                    SELECT ies.id_inimigo_setor INTO inimigo_setor_id
                    FROM Inimigo_Setor ies
                    WHERE ies.id_mob = inimigo_id
                    LIMIT 1;
                    
                    -- Reduzir quantidade atual se encontrado
                    IF inimigo_setor_id IS NOT NULL THEN
                        UPDATE Mob_Respawn_Control 
                        SET quantidade_atual = GREATEST(quantidade_atual - 1, 0)
                        WHERE id_inimigo_setor = inimigo_setor_id;
                    END IF;
                END IF;
            END IF;
            
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Recriar o trigger na tabela correta
    op.execute("""
        DROP TRIGGER IF EXISTS trigger_mob_morto_respawn ON Combate_Resultado;
        CREATE TRIGGER trigger_mob_morto_respawn
            AFTER INSERT ON Combate_Resultado
            FOR EACH ROW
            EXECUTE FUNCTION trigger_mob_morto();
    """)

def downgrade():
    # Remover trigger se necessário
    op.execute("DROP TRIGGER IF EXISTS trigger_mob_morto_respawn ON Combate_Resultado;")
    op.execute("DROP FUNCTION IF EXISTS trigger_mob_morto();")
