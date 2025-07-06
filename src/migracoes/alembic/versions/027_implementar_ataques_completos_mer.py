"""Implementar todos os ataques especiais conforme MER com custos de mana

Revision ID: 027
Revises: 026
Create Date: 2025-07-06

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '027'
down_revision = '026'
branch_labels = None
depends_on = None

def upgrade():
    # Limpar ataques existentes e implementar sistema completo conforme MER
    op.execute("""
        -- Limpar ataques existentes
        DELETE FROM Personagem_Ataque;
        DELETE FROM Ataque_Especial;
        
        -- ATAQUES JEDI (conforme MER) - 3 habilidades específicas
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Lightsaber Strike', 'Golpe preciso com sabre de luz', 25, 10, 1, 'Jedi', 'fisico', 'Ataque básico da classe Jedi'),
        ('Force Push', 'Empurra o inimigo usando a Força', 30, 20, 3, 'Jedi', 'forca', 'Pode atordoar o inimigo por 1 turno'),
        ('Force Heal', 'Cura ferimentos usando a Força', 0, 25, 5, 'Jedi', 'forca', 'Restaura 40 pontos de vida');
        
        -- ATAQUES SITH (conforme MER) - 3 habilidades específicas
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Dark Strike', 'Ataque sombrio com sabre vermelho', 25, 10, 1, 'Sith', 'fisico', 'Ataque básico da classe Sith'),
        ('Force Lightning', 'Dispara raios de energia sombria', 40, 25, 3, 'Sith', 'forca', 'Pode causar paralisia temporária'),
        ('Force Drain', 'Drena a energia vital do inimigo', 30, 30, 5, 'Sith', 'forca', 'Absorve 50% do dano como vida');
        
        -- ATAQUES CAÇADOR DE RECOMPENSAS (conforme MER) - 3 habilidades específicas
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Precise Shot', 'Tiro certeiro com blaster', 22, 8, 1, 'Cacador_de_Recompensas', 'tecnologico', 'Ataque básico da classe Caçador'),
        ('Explosive Grenade', 'Granada explosiva de alto impacto', 35, 20, 3, 'Cacador_de_Recompensas', 'tecnologico', 'Dano em área, pode atordoar'),
        ('Rapid Fire', 'Rajada rápida de múltiplos disparos', 45, 30, 5, 'Cacador_de_Recompensas', 'tecnologico', 'Múltiplos ataques em sequência');
    """)
    
    # Atualizar função desbloquear_ataques_iniciais para garantir que todos tenham ataque nível 1
    op.execute("""
        DROP FUNCTION IF EXISTS desbloquear_ataques_iniciais(INT);
        CREATE OR REPLACE FUNCTION desbloquear_ataques_iniciais(jogador_id INT)
        RETURNS TEXT AS $$
        DECLARE
            classe_jogador VARCHAR(50);
            ataques_desbloqueados INT := 0;
            resultado TEXT := '';
        BEGIN
            -- Obter classe do jogador
            SELECT nome_classe INTO classe_jogador
            FROM Personagem WHERE id_player = jogador_id;
            
            IF NOT FOUND THEN
                RETURN 'Erro: Jogador não encontrado';
            END IF;
            
            -- Desbloquear todos os ataques de nível 1 da classe
            INSERT INTO Personagem_Ataque (id_player, id_ataque, nivel_desbloqueio)
            SELECT jogador_id, ae.id_ataque, ae.nivel_requerido
            FROM Ataque_Especial ae
            WHERE ae.nome_classe = classe_jogador
              AND ae.nivel_requerido = 1
              AND NOT EXISTS (
                  SELECT 1 FROM Personagem_Ataque pa
                  WHERE pa.id_player = jogador_id AND pa.id_ataque = ae.id_ataque
              );
            
            GET DIAGNOSTICS ataques_desbloqueados = ROW_COUNT;
            
            IF ataques_desbloqueados > 0 THEN
                resultado := 'Ataques de nível 1 desbloqueados: ' || ataques_desbloqueados;
            ELSE
                resultado := 'Nenhum ataque novo desbloqueado';
            END IF;
            
            RETURN resultado;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Desbloquear ataques para todos os personagens existentes
    op.execute("""
        -- Desbloquear ataques para personagens existentes
        DO $$
        DECLARE
            personagem_record RECORD;
        BEGIN
            FOR personagem_record IN SELECT id_player FROM Personagem LOOP
                PERFORM desbloquear_ataques_iniciais(personagem_record.id_player);
            END LOOP;
        END $$;
    """)

def downgrade():
    # Reverter para ataques anteriores
    op.execute("""
        DELETE FROM Personagem_Ataque;
        DELETE FROM Ataque_Especial;
        
        -- Restaurar ataques anteriores (sem custos de mana)
        INSERT INTO Ataque_Especial (nome_ataque, descricao, dano_base, custo_mana, nivel_requerido, nome_classe, tipo_ataque, efeito_especial) VALUES
        ('Lightsaber Strike', 'Ataque básico com sabre de luz', 25, 0, 1, 'Jedi', 'fisico', 'Ataque básico sempre disponível'),
        ('Force Push', 'Empurra o inimigo usando a Força', 20, 15, 3, 'Jedi', 'forca', 'Pode atordoar o inimigo por 1 turno'),
        ('Force Heal', 'Cura ferimentos usando a Força', 0, 20, 5, 'Jedi', 'forca', 'Restaura 40 pontos de vida'),
        ('Dark Strike', 'Ataque básico com sabre vermelho', 25, 0, 1, 'Sith', 'fisico', 'Ataque básico sempre disponível'),
        ('Force Lightning', 'Dispara raios de energia sombria', 35, 18, 3, 'Sith', 'forca', 'Pode causar paralisia temporária'),
        ('Force Drain', 'Drena a energia vital do inimigo', 25, 22, 5, 'Sith', 'forca', 'Absorve 50% do dano como vida'),
        ('Precise Shot', 'Tiro certeiro com blaster', 22, 0, 1, 'Cacador_de_Recompensas', 'tecnologico', 'Ataque básico sempre disponível'),
        ('Explosive Grenade', 'Granada explosiva de alto impacto', 30, 16, 3, 'Cacador_de_Recompensas', 'tecnologico', 'Dano em área, pode atordoar'),
        ('Rapid Fire', 'Rajada rápida de múltiplos disparos', 40, 25, 5, 'Cacador_de_Recompensas', 'tecnologico', 'Múltiplos ataques em sequência');
    """)
