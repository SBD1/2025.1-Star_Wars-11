import psycopg2
import time
from MUD.jogo_starwars import JogoStarWars
def conectar_bd(max_tentativas=5):
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            conexao = psycopg2.connect(
                database="star_wars_db",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5433"
            )
            print("Conexão com o banco de dados estabelecida!")
            return conexao
        except Exception as e:
            print(f"Tentativa {tentativas + 1} de {max_tentativas}: {e}")
            tentativas += 1
            time.sleep(5) 
    return None

def testar_conexao():
    conexao = conectar_bd()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tabelas = cursor.fetchall()
        print("\nTabelas encontradas:")
        for tabela in tabelas:
            print(f"\n- Tabela: {tabela[0]}")
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{tabela[0]}'
            """)
            colunas = cursor.fetchall()
            for col in colunas:
                print(f"  └─ {col[0]} ({col[1]})")
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    print("Iniciando aplicação Star Wars MUD...")
    conexao = conectar_bd()
    if conexao:
        jogo = JogoStarWars(conexao)
        jogo.iniciar()
    else:
        print("Não foi possível conectar ao banco de dados.")