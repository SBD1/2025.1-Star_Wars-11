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
            print("missoes - Sistema de missões")
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
                self.menu_missoes()
            else:
                print("Comando não reconhecido!")

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

    def menu_missoes(self):
        """Menu principal de missões"""
        while True:
            print("\n=== Sistema de Missões ===")
            print("1. Ver missões disponíveis")
            print("2. Ver minhas missões")
            print("3. Aceitar missão")
            print("4. Concluir missão")
            print("5. Abandonar missão")
            print("6. Voltar")

            escolha = input("\nEscolha uma opção: ").strip()

            if escolha == "1":
                self.listar_missoes_disponiveis()
            elif escolha == "2":
                self.listar_minhas_missoes()
            elif escolha == "3":
                self.aceitar_missao()
            elif escolha == "4":
                self.concluir_missao()
            elif escolha == "5":
                self.abandonar_missao()
            elif escolha == "6":
                break
            else:
                print("Opção inválida!")

    def listar_missoes_disponiveis(self):
        """Lista missões disponíveis para o jogador atual"""
        cursor = self.conexao.cursor()
        try:
            # Buscar level e planeta do jogador
            cursor.execute("SELECT level, nome_planeta FROM Personagem WHERE id_player = %s", (self.jogador_atual,))
            jogador_info = cursor.fetchone()
            if not jogador_info:
                print("Erro: Jogador não encontrado")
                return

            jogador_level, jogador_planeta = jogador_info

            # Buscar todas as missões do planeta
            cursor.execute("""
                SELECT id_missao, nome_missao, descricao, valor_recompensa,
                       xp_recompensa, level_minimo, tipo_missao
                FROM Missao
                WHERE status = 'Disponível'
                  AND nome_planeta = %s
                  AND level_minimo <= %s
                ORDER BY level_minimo, valor_recompensa
            """, (jogador_planeta, jogador_level))

            todas_missoes = cursor.fetchall()

            # Buscar missões já aceitas pelo jogador
            cursor.execute("SELECT id_missao FROM Missao_Jogador WHERE id_player = %s", (self.jogador_atual,))
            missoes_aceitas = [row[0] for row in cursor.fetchall()]

            # Filtrar missões disponíveis
            missoes_disponiveis = [m for m in todas_missoes if m[0] not in missoes_aceitas]

            if not missoes_disponiveis:
                print(f"\n=== Nenhuma missão disponível em {jogador_planeta} ===")
                print("Viaje para outros planetas ou aumente seu level!")
                return

            print(f"\n=== Missões Disponíveis em {jogador_planeta} ===")
            for missao in missoes_disponiveis:
                print(f"\n[{missao[0]}] {missao[1]}")
                print(f"Descrição: {missao[2]}")
                print(f"Recompensa: {missao[3]} GCS + {missao[4]} XP")
                print(f"Level mínimo: {missao[5]} | Tipo: {missao[6]}")
                print("-" * 50)

        except Exception as erro:
            print(f"Erro ao listar missões: {erro}")
        finally:
            cursor.close()

    def listar_minhas_missoes(self):
        """Lista missões aceitas pelo jogador"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                SELECT mj.id_missao, m.nome_missao, mj.status_jogador,
                       m.tipo_missao, m.valor_recompensa, m.xp_recompensa
                FROM Missao_Jogador mj
                JOIN Missao m ON mj.id_missao = m.id_missao
                WHERE mj.id_player = %s
                ORDER BY mj.data_aceita DESC
            """, (self.jogador_atual,))

            missoes = cursor.fetchall()

            if not missoes:
                print("\n=== Você não possui missões ===")
                print("Use a opção 1 para ver missões disponíveis!")
                return

            print("\n=== Suas Missões ===")
            for missao in missoes:
                status_icon = "✓" if missao[2] == "Concluída" else "⏳"
                print(f"\n{status_icon} [{missao[0]}] {missao[1]}")
                print(f"Status: {missao[2]}")
                print(f"Tipo: {missao[3]} | Recompensa: {missao[4]} GCS + {missao[5]} XP")
                print("-" * 50)

        except Exception as erro:
            print(f"Erro ao listar suas missões: {erro}")
        finally:
            cursor.close()

    def aceitar_missao(self):
        """Permite ao jogador aceitar uma missão"""
        try:
            missao_id = int(input("\nDigite o ID da missão que deseja aceitar: "))

            cursor = self.conexao.cursor()

            # Verificar se a missão existe e está disponível
            cursor.execute("""
                SELECT m.nome_missao, m.level_minimo, m.nome_planeta, p.level, p.nome_planeta
                FROM Missao m, Personagem p
                WHERE m.id_missao = %s AND p.id_player = %s AND m.status = 'Disponível'
            """, (missao_id, self.jogador_atual))

            resultado = cursor.fetchone()
            if not resultado:
                print("Erro: Missão não encontrada ou não disponível")
                return

            missao_nome, missao_level, missao_planeta, jogador_level, jogador_planeta = resultado

            # Validações
            if jogador_level < missao_level:
                print(f"Erro: Level insuficiente. Necessário: {missao_level}, Atual: {jogador_level}")
                return

            if jogador_planeta != missao_planeta:
                print(f"Erro: Você precisa estar em {missao_planeta} para aceitar esta missão")
                return

            # Verificar se já aceitou
            cursor.execute("SELECT 1 FROM Missao_Jogador WHERE id_player = %s AND id_missao = %s",
                          (self.jogador_atual, missao_id))
            if cursor.fetchone():
                print("Erro: Você já aceitou esta missão")
                return

            # Aceitar a missão
            cursor.execute("""
                INSERT INTO Missao_Jogador (id_player, id_missao, status_jogador)
                VALUES (%s, %s, 'Em Andamento')
            """, (self.jogador_atual, missao_id))

            self.conexao.commit()
            print(f"Sucesso: Missão '{missao_nome}' aceita com sucesso!")

        except ValueError:
            print("Erro: Digite um número válido!")
        except Exception as erro:
            print(f"Erro ao aceitar missão: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()

    def concluir_missao(self):
        """Permite ao jogador concluir uma missão"""
        try:
            missao_id = int(input("\nDigite o ID da missão que deseja concluir: "))

            cursor = self.conexao.cursor()

            # Verificar se o jogador tem esta missão em andamento
            cursor.execute("""
                SELECT mj.status_jogador, m.valor_recompensa, m.xp_recompensa, m.nome_missao
                FROM Missao_Jogador mj
                JOIN Missao m ON mj.id_missao = m.id_missao
                WHERE mj.id_player = %s AND mj.id_missao = %s
            """, (self.jogador_atual, missao_id))

            resultado = cursor.fetchone()
            if not resultado:
                print("Erro: Você não possui esta missão")
                return

            status_atual, recompensa_gcs, recompensa_xp, missao_nome = resultado

            if status_atual != 'Em Andamento':
                print("Erro: Esta missão não está em andamento")
                return

            # Buscar dados atuais do jogador
            cursor.execute("SELECT gcs, xp, level FROM Personagem WHERE id_player = %s", (self.jogador_atual,))
            _, xp_atual, level_atual = cursor.fetchone()

            # Calcular novo level
            novo_xp = xp_atual + recompensa_xp
            novo_level = max(level_atual, novo_xp // 1000 + 1)

            # Atualizar jogador com recompensas
            cursor.execute("""
                UPDATE Personagem
                SET gcs = gcs + %s, xp = xp + %s, level = %s
                WHERE id_player = %s
            """, (recompensa_gcs, recompensa_xp, novo_level, self.jogador_atual))

            # Marcar missão como concluída
            cursor.execute("""
                UPDATE Missao_Jogador
                SET status_jogador = 'Concluída'
                WHERE id_player = %s AND id_missao = %s
            """, (self.jogador_atual, missao_id))

            self.conexao.commit()

            print(f"Sucesso: Missão '{missao_nome}' concluída!")
            print(f"Recompensas: {recompensa_gcs} GCS, {recompensa_xp} XP")
            if novo_level > level_atual:
                print(f"Level up! Novo level: {novo_level}")

        except ValueError:
            print("Erro: Digite um número válido!")
        except Exception as erro:
            print(f"Erro ao concluir missão: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()

    def abandonar_missao(self):
        """Permite ao jogador abandonar uma missão"""
        try:
            missao_id = int(input("\nDigite o ID da missão que deseja abandonar: "))

            cursor = self.conexao.cursor()

            # Verificar se o jogador tem esta missão
            cursor.execute("""
                SELECT mj.status_jogador, m.nome_missao
                FROM Missao_Jogador mj
                JOIN Missao m ON mj.id_missao = m.id_missao
                WHERE mj.id_player = %s AND mj.id_missao = %s
            """, (self.jogador_atual, missao_id))

            resultado = cursor.fetchone()
            if not resultado:
                print("Erro: Você não possui esta missão")
                return

            status_atual, missao_nome = resultado

            if status_atual == 'Concluída':
                print("Erro: Não é possível abandonar uma missão concluída")
                return

            # Remover a missão do jogador
            cursor.execute("""
                DELETE FROM Missao_Jogador
                WHERE id_player = %s AND id_missao = %s
            """, (self.jogador_atual, missao_id))

            self.conexao.commit()
            print(f"Missão '{missao_nome}' abandonada")

        except ValueError:
            print("Erro: Digite um número válido!")
        except Exception as erro:
            print(f"Erro ao abandonar missão: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()