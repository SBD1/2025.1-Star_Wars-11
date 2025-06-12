import psycopg2
import time

def connect_db(max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                database="star_wars_db",
                user="postgres",
                password="postgres",
                host="db",
                port="5432"
            )
            print("Conexão com o banco de dados estabelecida!")
            return conn
        except Exception as e:
            print(f"Tentativa {retries + 1} de {max_retries}: {e}")
            retries += 1
            time.sleep(5) 
    return None

def test_connection():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        # Lista todas as tabelas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print("\nTabelas encontradas:")
        for table in tables:
            print(f"\n- Tabela: {table[0]}")
            # Mostra estrutura de cada tabela
            cur.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table[0]}'
            """)
            columns = cur.fetchall()
            for col in columns:
                print(f"  └─ {col[0]} ({col[1]})")
        cur.close()
        conn.close()

if __name__ == "__main__":
    print("Iniciando aplicação Star Wars MUD...")
    while True:
        test_connection()
        print("\nServidor rodando")
        time.sleep(30) 