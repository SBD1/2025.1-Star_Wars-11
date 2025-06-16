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

    def menu_viagem(self):
        cursor = self.conexao.cursor()
        
        # Consulta melhorada para mostrar naves do jogador
        cursor.execute("""
            SELECT 
                n.modelo,
                n.velocidade,
                n.capacidade,
                CASE 
                    WHEN x.modelo IS NOT NULL THEN 'X-WING T-65'
                    WHEN y.modelo IS NOT NULL THEN 'YT-1300'
                    WHEN l.modelo IS NOT NULL THEN 'Lambda Shuttle'
                    WHEN f.modelo IS NOT NULL THEN 'Fregata CR90'
                END as tipo_nave
            FROM Nave n
            LEFT JOIN X_WING_T65 x ON n.modelo = x.modelo
            LEFT JOIN YT_1300 y ON n.modelo = y.modelo
            LEFT JOIN Lambda_Class_Shuttle l ON n.modelo = l.modelo
            LEFT JOIN Fregata_Corelliana_CR90 f ON n.modelo = f.modelo
            WHERE n.Id_Player = %s
        """, (self.jogador_atual,))
        
        naves = cursor.fetchall()
        if not naves:
            print("\nVocê precisa de uma nave para viajar!")
            return
        
        # Mostra naves disponíveis em formato tabular
        print("\n=== Suas Naves ===")
        print("Modelo          | Tipo            | Velocidade | Capacidade")
        print("-" * 60)
        for i, nave in enumerate(naves, 1):
            print(f"{i}. {nave[0]:<13} | {nave[3]:<14} | {nave[1]:<10} | {nave[2]}")
        
        # Pega planeta atual
        cursor.execute("""
            SELECT nome_planeta 
            FROM Personagem 
            WHERE id_player = %s
        """, (self.jogador_atual,))
        planeta_atual = cursor.fetchone()[0]
        
        # Lista planetas e requisitos
        cursor.execute("""
            SELECT p.nome_planeta, p.clima, 
                   CASE 
                       WHEN p.nome_planeta = 'Coruscant' THEN 150
                       WHEN p.nome_planeta = 'Tatooine' THEN 100
                       ELSE 0
                   END as velocidade_minima
            FROM Planeta p
            WHERE p.nome_planeta != %s
        """, (planeta_atual,))
        
        planetas = cursor.fetchall()
        print(f"\nVocê está em: {planeta_atual}")
        print("\nPlanetas disponíveis:")
        for planeta in planetas:
            req = f"(Requer nave com velocidade {planeta[2]})" if planeta[2] > 0 else "(Sem requisitos)"
            print(f"- {planeta[0]} | Clima: {planeta[1]} {req}")
        
        destino = input("\nPara qual planeta deseja viajar? ")
        
        # Seleção da nave por número
        try:
            escolha = int(input("\nEscolha o número da nave (1 para YT-1300 padrão): ")) - 1
            if 0 <= escolha < len(naves):
                nave_escolhida = naves[escolha][0]
            else:
                print("Número inválido. Usando YT-1300 padrão...")
                nave_escolhida = 'YT-1300-001'
        except ValueError:
            print("Entrada inválida. Usando YT-1300 padrão...")
            nave_escolhida = 'YT-1300-001'
    
        self.viajar_para_planeta(destino, nave_escolhida)
        cursor.close()

    def viajar_para_planeta(self, planeta_destino, nave_modelo):
        cursor = self.conexao.cursor()
        
        # Verifica se a nave pertence ao jogador
        cursor.execute("""
            SELECT velocidade 
            FROM Nave 
            WHERE modelo = %s AND Id_Player = %s
        """, (nave_modelo, self.jogador_atual))
        
        nave = cursor.fetchone()
        if not nave:
            print("Você não possui esta nave!")
            return
        
        # Verifica requisitos do planeta
        velocidade_minima = 0
        if planeta_destino == 'Coruscant':
            velocidade_minima = 150
        elif planeta_destino == 'Tatooine':
            velocidade_minima = 100
        
        if nave[0] < velocidade_minima:
            print(f"Sua nave é muito lenta para viajar para {planeta_destino}!");
            print(f"Velocidade mínima necessária: {velocidade_minima}");
            print(f"Velocidade da sua nave: {nave[0]}");
            return
        
        # Resto da lógica de viagem
        try:
            cursor.execute("""
                UPDATE Personagem 
                SET nome_planeta = %s 
                WHERE id_player = %s
            """, (planeta_destino, self.jogador_atual))
            
            self.conexao.commit()
            print(f"\nViagem concluída! Você chegou em {planeta_destino} usando {nave_modelo}")
            
        except Exception as erro:
            print(f"Erro ao viajar: {erro}")
            self.conexao.rollback()
    
        cursor.close()