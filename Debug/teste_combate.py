import psycopg2
import sys
import os

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from MUD.jogo_starwars import JogoStarWars

def testar_combate():
    try:
        print("Testando sistema de combate...")

        # Conectar ao banco
        conexao = psycopg2.connect(
            database="star_wars_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5433"
        )
        print("Conexão estabelecida!")
        
        # Criar instância do jogo
        jogo = JogoStarWars(conexao)
        jogo.jogador_atual = 1  # Simular jogador logado
        
        cursor = conexao.cursor()
        
        # Verificar se há combates ativos (limpar se houver)
        cursor.execute("DELETE FROM Combate WHERE id_player = %s AND status_combate = 'ativo'", (1,))
        conexao.commit()
        
        # Listar inimigos disponíveis
        cursor.execute("SELECT * FROM listar_inimigos_planeta(%s)", (1,))
        inimigos = cursor.fetchall()
        print(f"Inimigos disponíveis: {len(inimigos)}")

        if inimigos:
            inimigo_id = inimigos[0][0]  # Pegar o primeiro inimigo
            print(f"Testando combate contra inimigo ID: {inimigo_id}")

            # Testar iniciar combate
            cursor.execute("SELECT iniciar_combate(%s, %s)", (1, inimigo_id))
            resultado = cursor.fetchone()[0]
            print(f"Resultado iniciar combate: {resultado}")

            if resultado.startswith("Combate iniciado"):
                # Verificar se combate foi criado
                cursor.execute("SELECT id_combate FROM Combate WHERE id_player = %s AND status_combate = 'ativo'", (1,))
                combate = cursor.fetchone()

                if combate:
                    combate_id = combate[0]
                    print(f"Combate criado com ID: {combate_id}")

                    # Testar ação do jogador
                    cursor.execute("SELECT processar_turno_jogador(%s, %s)", (combate_id, 'ataque'))
                    resultado_ataque = cursor.fetchone()[0]
                    print(f"Resultado ataque: {resultado_ataque}")

                    # Testar turno do inimigo
                    cursor.execute("SELECT processar_turno_inimigo(%s)", (combate_id,))
                    resultado_inimigo = cursor.fetchone()[0]
                    print(f"Resultado turno inimigo: {resultado_inimigo}")

                    # Verificar status do combate
                    cursor.execute("SELECT * FROM obter_status_combate(%s)", (1,))
                    status = cursor.fetchone()
                    if status:
                        print(f"Status combate: Vida jogador={status[2]}, Vida inimigo={status[3]}, Turno={status[4]}")

                    # Finalizar combate para limpeza
                    cursor.execute("SELECT finalizar_combate(%s, %s)", (combate_id, 'jogador'))
                    resultado_fim = cursor.fetchone()[0]
                    print(f"Resultado finalizar: {resultado_fim}")

                else:
                    print("Combate não foi criado!")
            else:
                print(f"Erro ao iniciar combate: {resultado}")
        else:
            print("Nenhum inimigo disponível para teste!")
        
        cursor.close()
        conexao.close()
        
        print("\nTeste de combate concluído!")
        return True

    except Exception as e:
        print(f"Erro durante o teste de combate: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    testar_combate()
