class JogoStarWars:
    def __init__(self, conexao):
        self.conexao = conexao
        self.jogador_atual = None
    
    def iniciar(self):
        print("\n=== Star Wars MUD ===")
        while True:
            if not self.jogador_atual:
                self.mostrar_menu()
            else:
                self.loop_jogo()

    def mostrar_menu(self):
        print("\n1. Criar personagem")
        print("2. Carregar personagem")
        print("3. Deletar personagem")  
        print("4. Sair")
        
        escolha = input("\nEscolha uma opção: ")
        
        if escolha == "1":
            self.criar_personagem()
        elif escolha == "2":
            self.carregar_personagem()
        elif escolha == "3":
            self.deletar_personagem()  
        elif escolha == "4":
            exit()

    def criar_personagem(self):
        cursor = self.conexao.cursor()
        print("\n=== Criação de Personagem ===")
        
        cursor.execute("SELECT nome_classe FROM Classe")
        classes = cursor.fetchall()
        print("\nClasses disponíveis:")
        for classe in classes:
            print(f"- {classe[0]}")

        cursor.execute("SELECT nome_planeta FROM Planeta")
        planetas = cursor.fetchall()
        print("\nPlanetas disponíveis:")
        for planeta in planetas:
            print(f"- {planeta[0]}")

        classe = input("\nEscolha sua classe: ")
        planeta = input("Escolha seu planeta inicial: ")

        try:
            cursor.execute("""
                INSERT INTO Personagem (vida_base, level, dano_base, xp, gcs, nome_classe, nome_planeta) 
                VALUES (100, 1, 10, 0, 1000, %s, %s) RETURNING id_player
            """, (classe, planeta))
            
            self.jogador_atual = cursor.fetchone()[0]
            self.conexao.commit()
            print(f"\nPersonagem criado com sucesso! ID: {self.jogador_atual}")
            
        except Exception as erro:
            print(f"Erro ao criar personagem: {erro}")
            self.conexao.rollback()

        cursor.close()

    def carregar_personagem(self):
        id_jogador = input("\nDigite o ID do seu personagem: ")
        cursor = self.conexao.cursor()
        
        try:
            cursor.execute("""
                SELECT id_player, nome_classe, nome_planeta, level, vida_base, gcs 
                FROM Personagem 
                WHERE id_player = %s
            """, (id_jogador,))
            
            dados_jogador = cursor.fetchone()
            if dados_jogador:
                self.jogador_atual = dados_jogador[0]
                print(f"\nBem-vindo de volta!")
                print(f"Classe: {dados_jogador[1]}")
                print(f"Planeta: {dados_jogador[2]}")
                print(f"Level: {dados_jogador[3]}")
                print(f"Vida: {dados_jogador[4]}")
                print(f"GCS: {dados_jogador[5]}")
            else:
                print("Personagem não encontrado!")
                
        except Exception as erro:
            print(f"Erro ao carregar personagem: {erro}")
        
        cursor.close()

    def loop_jogo(self):
        while True:
            print("\n=== Comandos ===")
            print("status - Ver status do personagem")
            print("viajar - Viajar para outro planeta")
            print("missoes - Ver missões disponíveis")
            print("sair - Sair do jogo")
            
            comando = input("\n> ").lower().strip()
            
            if comando == "sair":
                self.jogador_atual = None
                break
            elif comando == "status":
                self.mostrar_status()
            elif comando == "viajar":
                self.menu_viagem()
            elif comando == "missoes":
                self.mostrar_missoes()

    def mostrar_status(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT nome_classe, nome_planeta, level, vida_base, gcs 
            FROM Personagem 
            WHERE id_player = %s
        """, (self.jogador_atual,))
        
        status = cursor.fetchone()
        print("\n=== Status do Personagem ===")
        print(f"Classe: {status[0]}")
        print(f"Planeta atual: {status[1]}")
        print(f"Level: {status[2]}")
        print(f"Vida: {status[3]}")
        print(f"GCS: {status[4]}")
        cursor.close()

    def deletar_personagem(self):
        id_jogador = input("\nDigite o ID do personagem que deseja deletar: ")
        cursor = self.conexao.cursor()
        
        try:
            cursor.execute("""
                DELETE FROM Personagem 
                WHERE id_player = %s
                RETURNING id_player
            """, (id_jogador,))
            
            if cursor.fetchone():
                self.conexao.commit()
                print(f"Personagem {id_jogador} deletado com sucesso!")
                if self.jogador_atual == int(id_jogador):
                    self.jogador_atual = None
            else:
                print("Personagem não encontrado!")
                
        except Exception as erro:
            print(f"Erro ao deletar personagem: {erro}")
            self.conexao.rollback()
        
        cursor.close()