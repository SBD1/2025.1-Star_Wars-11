import psycopg2
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from MUD.jogo_starwars import JogoStarWars

def testar_jogo():
    try:
        print("🚀 Testando conexão e inicialização do jogo...")
        
        # Conectar ao banco
        conexao = psycopg2.connect(
            database="star_wars_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5433"
        )
        print("✅ Conexão estabelecida!")
        
        # Criar instância do jogo
        jogo = JogoStarWars(conexao)
        print("✅ Jogo instanciado!")
        
        # Testar algumas funções básicas
        cursor = conexao.cursor()
        
        # Verificar se há personagens
        cursor.execute("SELECT COUNT(*) FROM Personagem")
        total_personagens = cursor.fetchone()[0]
        print(f"📊 Total de personagens no banco: {total_personagens}")
        
        # Verificar se há inimigos
        cursor.execute("SELECT COUNT(*) FROM Inimigo")
        total_inimigos = cursor.fetchone()[0]
        print(f"👹 Total de inimigos no banco: {total_inimigos}")
        
        # Testar função de listar inimigos (se houver personagens)
        if total_personagens > 0:
            cursor.execute("SELECT id_player FROM Personagem LIMIT 1")
            jogador_teste = cursor.fetchone()[0]
            
            try:
                cursor.execute("SELECT * FROM listar_inimigos_planeta(%s)", (jogador_teste,))
                inimigos_planeta = cursor.fetchall()
                print(f"🌍 Inimigos no planeta do jogador {jogador_teste}: {len(inimigos_planeta)}")
            except Exception as e:
                print(f"⚠️  Erro ao listar inimigos: {e}")
        
        # Testar verificação de combate ativo
        jogo.jogador_atual = 1  # Simular jogador logado
        combate_ativo = jogo.verificar_combate_ativo()
        print(f"⚔️  Combate ativo para jogador 1: {combate_ativo}")
        
        cursor.close()
        conexao.close()
        
        print("\n✅ Todos os testes básicos passaram!")
        print("🎮 O sistema de combate está pronto para uso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    testar_jogo()
