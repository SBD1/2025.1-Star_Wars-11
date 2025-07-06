import psycopg2

def testar_tipos_mob():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='starwars_db',
            user='postgres',
            password='postgres',
            port='5432'
        )
        cur = conn.cursor()

        print('=== TESTE: TIPOS DE MOB ===\n')

        # Testar função obter_tipo_mob
        print('1. Testando função obter_tipo_mob:')
        mobs = ['Stormtrooper', 'Dark Trooper', 'Rancor']
        for mob in mobs:
            cur.execute("SELECT obter_tipo_mob(%s)", (mob,))
            tipo = cur.fetchone()[0]
            print(f'   {mob}: {tipo}')

        print('\n2. Testando função obter_caracteristicas_mob:')
        for mob in mobs:
            cur.execute("SELECT obter_caracteristicas_mob(%s)", (mob,))
            caracteristicas = cur.fetchone()[0]
            print(f'   {mob}: {caracteristicas}')

        print('\n3. Testando listagem de inimigos com tipos:')
        # Assumindo que existe pelo menos um personagem
        cur.execute("SELECT id_player FROM Personagem LIMIT 1")
        jogador = cur.fetchone()
        
        if jogador:
            jogador_id = jogador[0]
            cur.execute("SELECT * FROM listar_inimigos_planeta(%s)", (jogador_id,))
            inimigos = cur.fetchall()
            
            print('   ID | Tipo           | Vida | Nível | Dano | Categoria')
            print('   ' + '-' * 55)
            for inimigo in inimigos:
                id_mob, tipo, vida, nivel, dano, escudo, creditos, ameaca, categoria = inimigo
                simbolo = {"Normal": "⚔️", "Elite": "🛡️", "Boss": "👑"}.get(categoria, "❓")
                print(f'   {id_mob:<2} | {tipo:<13} | {vida:<4} | {nivel:<5} | {dano:<4} | {simbolo} {categoria}')
        else:
            print('   Nenhum personagem encontrado para teste')

        print('\n✅ Teste concluído com sucesso!')
        
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f'❌ Erro durante o teste: {e}')
        return False

if __name__ == "__main__":
    testar_tipos_mob()
