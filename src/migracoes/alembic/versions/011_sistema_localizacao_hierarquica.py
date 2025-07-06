"""Sistema de localização hierárquica - Planetas → Cidades → Setores

Revision ID: 011
Revises: 010
Create Date: 2025-01-05 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '011'
down_revision = '010'
branch_labels = None
depends_on = None

def upgrade():
    """Implementa sistema de localização hierárquica com inimigos fixos nos setores"""
    
    print("Criando sistema de localização hierárquica...")

    import os

    # Navegar para o diretório DDL a partir do diretório de migrações
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ddl_dir = os.path.join(current_dir, '..', '..', '..', 'DDL')

    # Executar script de criação das tabelas e dados
    ddl_path = os.path.join(ddl_dir, 'ddl_localizacao_hierarquica.sql')
    with open(ddl_path, 'r', encoding='utf-8') as f:
        ddl_content = f.read()

    op.execute(ddl_content)

    # Executar script de funções de localização
    funcoes_path = os.path.join(ddl_dir, 'ddl_funcoes_localizacao.sql')
    with open(funcoes_path, 'r', encoding='utf-8') as f:
        funcoes_content = f.read()

    op.execute(funcoes_content)

    # Atualizar funções de combate para trabalhar com setores
    combate_path = os.path.join(ddl_dir, 'ddl_funcoes_combate.sql')
    with open(combate_path, 'r', encoding='utf-8') as f:
        combate_content = f.read()

    op.execute(combate_content)
    
    # Inicializar localização dos jogadores existentes
    op.execute("""
        -- Colocar jogadores existentes no primeiro setor de seus planetas
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
    
    print("Sistema de localização hierárquica implementado com sucesso!")
    print("- Criadas tabelas: Cidade, Setor, Inimigo_Setor")
    print("- Adicionada coluna id_setor na tabela Personagem")
    print("- Criadas funções de navegação e combate por setor")
    print("- Inimigos agora são fixos em setores específicos")
    print("- Sistema de respawn implementado")

def downgrade():
    """Remove o sistema de localização hierárquica"""
    
    print("Removendo sistema de localização hierárquica...")
    
    # Remover funções
    op.execute("""
        -- Remover funções de localização
        DROP FUNCTION IF EXISTS inicializar_localizacao_jogador(INT, VARCHAR(20));
        DROP FUNCTION IF EXISTS derrotar_inimigo_setor(INT, INT);
        DROP FUNCTION IF EXISTS processar_respawn_inimigos();
        DROP FUNCTION IF EXISTS obter_localizacao_jogador(INT);
        DROP FUNCTION IF EXISTS mover_jogador_setor(INT, INT);
        DROP FUNCTION IF EXISTS listar_inimigos_setor(INT);
        DROP FUNCTION IF EXISTS listar_setores_cidade(INT);
        DROP FUNCTION IF EXISTS listar_cidades_planeta(VARCHAR(20));
        
        -- Remover funções de combate atualizadas
        DROP FUNCTION IF EXISTS listar_inimigos_setor_jogador(INT);
    """)
    
    # Restaurar função original de combate
    op.execute("""
        -- Restaurar função original de listar inimigos por planeta
        CREATE OR REPLACE FUNCTION listar_inimigos_planeta(jogador_id INT)
        RETURNS TABLE (
            id_mob INT,
            tipo_mob VARCHAR(22),
            vida_base INT,
            nivel INT,
            dano_base INT,
            pontos_escudo INT,
            creditos INT,
            nivel_ameaca INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                i.id_mob,
                i.tipo_mob,
                i.vida_base,
                i.nivel,
                i.dano_base,
                i.pontos_escudo,
                i.creditos,
                m.nivel_ameaca
            FROM Inimigo i
            JOIN MOB m ON i.tipo_mob = m.tipo_mob
            JOIN Personagem p ON p.nome_planeta = i.planeta_origem
            WHERE p.id_player = jogador_id
            ORDER BY m.nivel_ameaca, i.nivel;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Remover coluna da tabela Personagem
    op.drop_constraint('fk_personagem_setor', 'personagem', type_='foreignkey')
    op.drop_column('personagem', 'id_setor')
    
    # Remover tabelas (ordem inversa devido às foreign keys)
    op.drop_table('inimigo_setor')
    op.drop_table('setor')
    op.drop_table('cidade')
    
    print("Sistema de localização hierárquica removido!")
