import psycopg2
import time

def testar_conexao():
    try:
        print("Tentando conectar ao banco...")
        conexao = psycopg2.connect(
            database="star_wars_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5433"
        )
        print("✅ Conexão estabelecida com sucesso!")
        
        cursor = conexao.cursor()
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()
        print(f"Versão do PostgreSQL: {versao[0]}")
        
        # Testar se as tabelas existem
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tabelas = cursor.fetchall()
        print(f"\nTabelas encontradas ({len(tabelas)}):")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        
        # Verificar se as tabelas de combate existem
        tabelas_combate = ['combate', 'combate_log', 'combate_resultado']
        for tabela in tabelas_combate:
            cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = '{tabela}'
                );
            """)
            existe = cursor.fetchone()[0]
            status = "✅" if existe else "❌"
            print(f"  {status} Tabela {tabela}: {'Existe' if existe else 'Não existe'}")
        
        cursor.close()
        conexao.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    testar_conexao()
