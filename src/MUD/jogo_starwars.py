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

    def _selecionar_opcao_por_numero(self, titulo, opcoes, prompt):
        print(f"\n{titulo}")
        for i, opcao in enumerate(opcoes, 1):
            print(f"{i}. {opcao[0]}")

        while True: 
            try:
                escolha_num = int(input(f"\n{prompt}"))
                
                if 1 <= escolha_num <= len(opcoes):
                    return opcoes[escolha_num - 1][0]
                else:
                    print("Opção inválida. Por favor, escolha um número da lista.")
            except ValueError:
                print("Entrada inválida. Por favor, digite apenas o número.")

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
        
        cursor.execute("SELECT nome_planeta FROM Planeta")
        planetas = cursor.fetchall()

        classe_escolhida = self._selecionar_opcao_por_numero(
            "Classes disponíveis:", 
            classes, 
            "Escolha o número da sua classe: "
        )

        planeta_escolhido = self._selecionar_opcao_por_numero(
            "Planetas disponíveis:", 
            planetas, 
            "Escolha o número do seu planeta inicial: "
        )

        try:
            cursor.execute("""
                INSERT INTO Personagem (vida_base, level, dano_base, xp, gcs, nome_classe, nome_planeta) 
                VALUES (100, 1, 10, 0, 1000, %s, %s) RETURNING id_player
            """, (classe_escolhida, planeta_escolhido))
            
            self.jogador_atual = cursor.fetchone()[0]
            self.conexao.commit()
            print(f"\nPersonagem '{classe_escolhida}' criado em '{planeta_escolhido}' com sucesso! ID: {self.jogador_atual}")
            
        except Exception as erro:
            print(f"Erro ao criar personagem: {erro}")
            self.conexao.rollback()

        cursor.close()


    def carregar_personagem(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id_player, nome_classe, nome_planeta FROM Personagem")
        personagens = cursor.fetchall()
        print("\n=== Carregar Personagem ===\n")

        for personagem in personagens:
            print(f"ID: {personagem[0]}, Classe: {personagem[1]}, Planeta: {personagem[2]}")

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
            # Verificar se jogador está em combate
            if self.verificar_combate_ativo():
                self.menu_combate_ativo()
                continue

            print("\n=== Comandos ===")
            print("1. status - Ver status do personagem")
            print("2. mapa - Ver localização atual e navegar")
            print("3. viajar - Viajar para outro planeta")
            print("4. missoes - Ver missões disponíveis")
            print("5. combate - Iniciar combate")
            print("6. sair - Sair do jogo")

            comando = input("\n> ").lower().strip()

            if comando == "6":
                self.jogador_atual = None
                print("\nSessão encerrada. Voltando para o menu principal...")
                break
            elif comando == "1":
                self.mostrar_status()
            elif comando == "2":
                self.menu_mapa()
            elif comando == "3":
                self.menu_viagem()
            elif comando == "4":
                self.menu_missoes()
            elif comando == "5":
                self.menu_combate()
            else:
                print("Comando não reconhecido!")

    def mostrar_status(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT nome_classe, nome_planeta, level, vida_atual, vida_base, gcs
            FROM Personagem
            WHERE id_player = %s
        """, (self.jogador_atual,))

        status = cursor.fetchone()
        print("\n=== Status do Personagem ===")
        print(f"Classe: {status[0]}")
        print(f"Planeta atual: {status[1]}")
        print(f"Level: {status[2]}")
        print(f"Vida: {status[3]}/{status[4]}")  # vida_atual/vida_base
        print(f"GCS: {status[5]}")
        cursor.close()

    def deletar_personagem(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id_player, nome_classe, nome_planeta FROM Personagem")
        personagens = cursor.fetchall()
        print("\n=== Deletar Personagem ===\n")
        
        for personagem in personagens:
            print(f"ID: {personagem[0]}, Classe: {personagem[1]}, Planeta: {personagem[2]}")


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
        # 1. Abrindo o cursor manualmente no início
        cursor = self.conexao.cursor()
        try:
            # Todo o código que usa o cursor fica dentro do bloco 'try'

            # Consulta para mostrar naves do jogador
            cursor.execute("""
                SELECT 
                    n.modelo, n.velocidade, n.capacidade,
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
                return # O 'finally' será executado mesmo com este 'return'
            
            # Mostra naves disponíveis
            print("\n=== Suas Naves ===")
            print("Modelo          | Tipo            | Velocidade | Capacidade")
            print("-" * 60)
            for i, nave in enumerate(naves, 1):
                print(f"{i}. {nave[0]:<13} | {nave[3]:<14} | {nave[1]:<10} | {nave[2]}")
            
            # Pega planeta atual
            cursor.execute("SELECT nome_planeta FROM Personagem WHERE id_player = %s", (self.jogador_atual,))
            planeta_atual = cursor.fetchone()[0]
            
            # Lista planetas disponíveis
            cursor.execute("""
                SELECT p.nome_planeta, p.clima
                FROM Planeta p
                WHERE p.nome_planeta != %s
            """, (planeta_atual,))

            planetas = cursor.fetchall()
            print(f"\nVocê está em: {planeta_atual}")
            print("\nPlanetas disponíveis:")
            for i, planeta in enumerate(planetas, 1):
                print(f"{i}. {planeta[0]} | Clima: {planeta[1]}")
            
            # Pede o número do planeta e valida
            destino_escolhido = None
            while True:
                try:
                    escolha_planeta = int(input("\nEscolha o número do planeta para o qual deseja viajar: "))
                    if 1 <= escolha_planeta <= len(planetas):
                        destino_escolhido = planetas[escolha_planeta - 1][0]
                        break
                    else:
                        print("Opção inválida. Por favor, escolha um número da lista.")
                except ValueError:
                    print("Entrada inválida. Por favor, digite apenas o número.")

            # Seleção da nave por número
            nave_escolhida = None
            if len(naves) == 1:
                nave_escolhida = naves[0][0]
                print(f"\nUsando sua única nave: {nave_escolhida}")
            else:
                 try:
                    escolha_nave = int(input("\nEscolha o número da nave que deseja usar: ")) - 1
                    if 0 <= escolha_nave < len(naves):
                        nave_escolhida = naves[escolha_nave][0]
                    else:
                        print("Número da nave inválido. Operação cancelada.")
                        return # O 'finally' também será executado aqui
                 except ValueError:
                    print("Entrada inválida. Operação cancelada.")
                    return # E aqui também

            # Chama a função de viajar
            # Como essa função abre seu próprio cursor, não há problema em chamá-la aqui
            self.viajar_para_planeta(destino_escolhido)
            
        finally:
            # 2. O bloco 'finally' garante que o cursor será fechado, não importa o que aconteça
            cursor.close()

    def viajar_para_planeta(self, planeta_destino):
        cursor = self.conexao.cursor()

        try:
            # A função do banco agora faz toda a validação, incluindo velocidade e nave
            cursor.execute("SELECT viajar_para_planeta(%s, %s)", (self.jogador_atual, planeta_destino))
            resultado = cursor.fetchone()[0]

            self.conexao.commit()
            print(f"\n{resultado}")

        except Exception as erro:
            print(f"Erro ao viajar: {erro}")
            self.conexao.rollback()
        finally:
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

    # =====================================================
    # SISTEMA DE COMBATE
    # =====================================================

    def verificar_combate_ativo(self):
        """Verifica se o jogador está em combate ativo"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                SELECT id_combate FROM Combate
                WHERE id_player = %s AND status_combate = 'ativo'
            """, (self.jogador_atual,))

            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            cursor.close()

    def menu_combate(self):
        """Menu principal de combate"""
        cursor = self.conexao.cursor()
        try:
            # Listar inimigos disponíveis no setor atual
            cursor.execute("SELECT * FROM listar_inimigos_setor_jogador(%s)", (self.jogador_atual,))
            inimigos = cursor.fetchall()

            if not inimigos:
                print("\n=== Nenhum inimigo encontrado ===")
                print("Não há inimigos disponíveis no seu planeta atual.")
                return

            print("\n=== Inimigos Disponíveis ===")
            print("ID  | Tipo               | Vida | Nível | Dano | Escudo | Créditos | Ameaça")
            print("-" * 75)

            for inimigo in inimigos:
                print(f"{inimigo[0]:<3} | {inimigo[1]:<17} | {inimigo[2]:<4} | {inimigo[3]:<5} | {inimigo[4]:<4} | {inimigo[5]:<6} | {inimigo[6]:<8} | {inimigo[7]}")

            print("\nEscolha um inimigo para combater ou digite 0 para voltar:")

            try:
                escolha = int(input("> "))
                if escolha == 0:
                    return

                # Verificar se o ID do inimigo é válido
                inimigo_escolhido = None
                for inimigo in inimigos:
                    if inimigo[0] == escolha:
                        inimigo_escolhido = inimigo
                        break

                if not inimigo_escolhido:
                    print("ID de inimigo inválido!")
                    return

                # Iniciar combate
                self.iniciar_combate(escolha)

            except ValueError:
                print("Digite um número válido!")

        except Exception as erro:
            print(f"Erro no menu de combate: {erro}")
        finally:
            cursor.close()

    def iniciar_combate(self, inimigo_id):
        """Inicia um combate contra um inimigo"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT iniciar_combate(%s, %s)", (self.jogador_atual, inimigo_id))
            resultado = cursor.fetchone()[0]
            self.conexao.commit()  # Commit da transação

            print(f"\n{resultado}")

            if resultado.startswith("Combate iniciado"):
                print("\nCOMBATE INICIADO!")
                print("Use os comandos de combate para lutar!")

        except Exception as erro:
            print(f"Erro ao iniciar combate: {erro}")
        finally:
            cursor.close()

    def menu_combate_ativo(self):
        """Menu para quando o jogador está em combate ativo"""
        cursor = self.conexao.cursor()
        try:
            # Obter status do combate atual
            cursor.execute("SELECT * FROM obter_status_combate(%s)", (self.jogador_atual,))
            status = cursor.fetchone()

            if not status:
                print("Erro: Combate não encontrado!")
                return

            combate_id, tipo_inimigo, vida_jogador, vida_inimigo, turno_atual, turno_numero = status

            print("\n" + "="*50)
            print("COMBATE EM ANDAMENTO")
            print("="*50)
            print(f"Inimigo: {tipo_inimigo}")
            print(f"Sua vida: {vida_jogador} HP")
            print(f"Vida do inimigo: {vida_inimigo} HP")
            print(f"Turno #{turno_numero + 1}")
            print("-"*50)

            if turno_atual == 'jogador':
                print("É o seu turno!")
                print("\nAções disponíveis:")
                print("1. Atacar")
                print("2. Defender")
                print("3. Fugir")

                try:
                    escolha = input("\nEscolha sua ação: ").strip()

                    if escolha == "1":
                        self.processar_acao_jogador(combate_id, "ataque")
                    elif escolha == "2":
                        self.processar_acao_jogador(combate_id, "defesa")
                    elif escolha == "3":
                        self.processar_acao_jogador(combate_id, "fuga")
                    else:
                        print("Ação inválida!")

                except Exception as erro:
                    print(f"Erro ao processar ação: {erro}")
            else:
                print("Turno do inimigo...")
                input("Pressione Enter para continuar...")
                self.processar_turno_inimigo(combate_id)

        except Exception as erro:
            print(f"Erro no combate: {erro}")
        finally:
            cursor.close()

    def processar_acao_jogador(self, combate_id, acao):
        """Processa a ação do jogador no combate"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT processar_turno_jogador(%s, %s)", (combate_id, acao))
            resultado = cursor.fetchone()[0]
            self.conexao.commit()  # Commit da transação

            print(f"\n{resultado}")

            # Se não fugiu, processar turno do inimigo
            if not resultado.startswith("Voce fugiu") and not "derrotado" in resultado:
                input("\nPressione Enter para o turno do inimigo...")
                self.processar_turno_inimigo(combate_id)
            elif resultado.startswith("Voce fugiu"):
                # Se fugiu com sucesso, apenas aguardar confirmação
                input("\nPressione Enter para continuar...")
                return  # Sair da função sem processar turno do inimigo

        except Exception as erro:
            print(f"Erro ao processar ação do jogador: {erro}")
        finally:
            cursor.close()

    def processar_turno_inimigo(self, combate_id):
        """Processa o turno do inimigo"""
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT processar_turno_inimigo(%s)", (combate_id,))
            resultado = cursor.fetchone()[0]
            self.conexao.commit()  # Commit da transação

            print(f"\n{resultado}")

            if not "derrotado" in resultado:
                input("\nPressione Enter para continuar...")

        except Exception as erro:
            print(f"Erro ao processar turno do inimigo: {erro}")

    def menu_mapa(self):
        """Menu para visualizar localização atual e navegar entre cidades/setores"""
        cursor = self.conexao.cursor()

        try:
            while True:
                # Obter localização atual do jogador (atualizada a cada loop)
                cursor.execute("SELECT * FROM obter_localizacao_jogador(%s)", (self.jogador_atual,))
                localizacao = cursor.fetchone()

                if not localizacao:
                    print("Erro: Não foi possível obter sua localização atual.")
                    return

                planeta, cidade, setor, id_setor_atual, tipo_setor, nivel_perigo, descricao_setor = localizacao

                print(f"\n=== MAPA - Sua Localização ===")
                print(f"Planeta: {planeta}")
                print(f"Cidade: {cidade}")
                print(f"Setor: {setor}")
                print(f"Tipo: {tipo_setor} | Nível de Perigo: {nivel_perigo}")
                print(f"Descrição: {descricao_setor}")

                print(f"\n=== Opções de Navegação ===")
                print("1. Ver cidades do planeta")
                print("2. Ver setores da cidade atual")
                print("3. Mover para outro setor")
                print("4. Viajar para outra cidade")
                print("5. sair")

                opcao = input("\n> ").strip()

                if opcao == "5":
                    break
                elif opcao == "1":
                    self.listar_cidades_planeta(planeta)
                elif opcao == "2":
                    self.listar_setores_cidade_atual(cidade)
                elif opcao == "3":
                    self.mover_para_setor()
                elif opcao == "4":
                    self.viajar_para_cidade()
                else:
                    print("Opção inválida!")

        except Exception as erro:
            print(f"Erro no menu mapa: {erro}")
        finally:
            cursor.close()

    def listar_cidades_planeta(self, planeta):
        """Lista todas as cidades do planeta atual"""
        cursor = self.conexao.cursor()

        try:
            cursor.execute("SELECT * FROM listar_cidades_planeta(%s)", (planeta,))
            cidades = cursor.fetchall()

            if not cidades:
                print(f"Nenhuma cidade encontrada no planeta {planeta}.")
                return

            print(f"\n=== Cidades de {planeta} ===")
            print("ID  | Nome                    | Setores | Descrição")
            print("-" * 65)

            for cidade in cidades:
                id_cidade, nome_cidade, descricao, total_setores = cidade
                print(f"{id_cidade:<3} | {nome_cidade:<22} | {total_setores:<7} | {descricao[:30]}...")

        except Exception as erro:
            print(f"Erro ao listar cidades: {erro}")
        finally:
            cursor.close()

    def listar_setores_cidade_atual(self, cidade):
        """Lista todos os setores da cidade atual"""
        cursor = self.conexao.cursor()

        try:
            # Primeiro obter o ID da cidade
            cursor.execute("SELECT id_cidade FROM Cidade WHERE nome_cidade = %s", (cidade,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"Cidade {cidade} não encontrada.")
                return

            id_cidade = resultado[0]

            cursor.execute("SELECT * FROM listar_setores_cidade(%s)", (id_cidade,))
            setores = cursor.fetchall()

            if not setores:
                print(f"Nenhum setor encontrado na cidade {cidade}.")
                return

            print(f"\n=== Setores de {cidade} ===")
            print("ID  | Nome                    | Tipo        | Perigo | Inimigos | Descrição")
            print("-" * 80)

            for setor in setores:
                id_setor, nome_setor, descricao, tipo_setor, nivel_perigo, total_inimigos, inimigos_ativos = setor
                print(f"{id_setor:<3} | {nome_setor:<22} | {tipo_setor:<10} | {nivel_perigo:<6} | {inimigos_ativos:<8} | {descricao[:20]}...")

        except Exception as erro:
            print(f"Erro ao listar setores: {erro}")
        finally:
            cursor.close()

    def mover_para_setor(self):
        """Move o jogador para outro setor"""
        cursor = self.conexao.cursor()

        try:
            # Primeiro mostrar setores disponíveis
            cursor.execute("SELECT * FROM obter_localizacao_jogador(%s)", (self.jogador_atual,))
            localizacao = cursor.fetchone()

            if not localizacao:
                print("Erro: Não foi possível obter sua localização atual.")
                return

            cidade = localizacao[1]  # nome da cidade

            # Obter ID da cidade
            cursor.execute("SELECT id_cidade FROM Cidade WHERE nome_cidade = %s", (cidade,))
            resultado = cursor.fetchone()

            if not resultado:
                print(f"Cidade {cidade} não encontrada.")
                return

            id_cidade = resultado[0]

            # Listar setores
            cursor.execute("SELECT * FROM listar_setores_cidade(%s)", (id_cidade,))
            setores = cursor.fetchall()

            if not setores:
                print(f"Nenhum setor encontrado na cidade {cidade}.")
                return

            print(f"\n=== Setores Disponíveis em {cidade} ===")
            print("ID  | Nome                    | Tipo        | Perigo | Inimigos")
            print("-" * 65)

            for setor in setores:
                id_setor, nome_setor, descricao, tipo_setor, nivel_perigo, total_inimigos, inimigos_ativos = setor
                print(f"{id_setor:<3} | {nome_setor:<22} | {tipo_setor:<10} | {nivel_perigo:<6} | {inimigos_ativos}")

            setor_id = input("\nDigite o ID do setor para onde deseja se mover (0 para cancelar): ").strip()

            if setor_id == "0":
                return

            try:
                setor_id = int(setor_id)
            except ValueError:
                print("ID inválido!")
                return

            # Mover jogador
            cursor.execute("SELECT mover_jogador_setor(%s, %s)", (self.jogador_atual, setor_id))
            resultado = cursor.fetchone()[0]

            # COMMIT da transação para persistir a mudança
            self.conexao.commit()

            print(f"\n{resultado}")

        except Exception as erro:
            print(f"Erro ao mover para setor: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()

    def viajar_para_cidade(self):
        """Viaja para outra cidade do mesmo planeta"""
        cursor = self.conexao.cursor()

        try:
            # Obter planeta atual
            cursor.execute("SELECT * FROM obter_localizacao_jogador(%s)", (self.jogador_atual,))
            localizacao = cursor.fetchone()

            if not localizacao:
                print("Erro: Não foi possível obter sua localização atual.")
                return

            planeta = localizacao[0]

            # Listar cidades do planeta
            cursor.execute("SELECT * FROM listar_cidades_planeta(%s)", (planeta,))
            cidades = cursor.fetchall()

            if not cidades:
                print(f"Nenhuma cidade encontrada no planeta {planeta}.")
                return

            print(f"\n=== Cidades Disponíveis em {planeta} ===")
            print("ID  | Nome                    | Setores | Descrição")
            print("-" * 65)

            for cidade in cidades:
                id_cidade, nome_cidade, descricao, total_setores = cidade
                print(f"{id_cidade:<3} | {nome_cidade:<22} | {total_setores:<7} | {descricao[:30]}...")

            cidade_id = input("\nDigite o ID da cidade para onde deseja viajar (0 para cancelar): ").strip()

            if cidade_id == "0":
                return

            try:
                cidade_id = int(cidade_id)
            except ValueError:
                print("ID inválido!")
                return

            # Viajar para cidade
            cursor.execute("SELECT viajar_para_cidade(%s, %s)", (self.jogador_atual, cidade_id))
            resultado = cursor.fetchone()[0]

            # COMMIT da transação para persistir a mudança
            self.conexao.commit()

            print(f"\n{resultado}")

        except Exception as erro:
            print(f"Erro ao viajar para cidade: {erro}")
            self.conexao.rollback()
        finally:
            cursor.close()