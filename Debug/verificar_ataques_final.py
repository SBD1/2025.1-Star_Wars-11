import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='starwars_db',
    user='postgres',
    password='postgres',
    port='5432'
)
cur = conn.cursor()

print('=== ATAQUES ESPECIAIS POR CLASSE (FINAL) ===')
cur.execute('''
    SELECT nome_classe, nome_ataque, nivel_requerido, dano_base, custo_mana, tipo_ataque, efeito_especial
    FROM Ataque_Especial 
    ORDER BY nome_classe, nivel_requerido, nome_ataque
''')
ataques = cur.fetchall()

classe_atual = None
for classe, nome, nivel, dano, mana, tipo, efeito in ataques:
    if classe != classe_atual:
        print(f'\n--- {classe} ---')
        classe_atual = classe
    print(f'  Nível {nivel}: {nome} (Dano: {dano}, Força: {mana}, Tipo: {tipo})')
    print(f'    Efeito: {efeito}')

print('\n=== CONTAGEM POR CLASSE ===')
cur.execute('''
    SELECT nome_classe, COUNT(*) as total
    FROM Ataque_Especial 
    GROUP BY nome_classe
    ORDER BY nome_classe
''')
contagem = cur.fetchall()

for classe, total in contagem:
    print(f'{classe}: {total} ataques')

print('\n=== ATAQUES DESBLOQUEADOS POR PERSONAGEM ===')
cur.execute('''
    SELECT p.id_player, p.nome_classe, p.level, COUNT(pa.id_ataque) as ataques_desbloqueados
    FROM Personagem p
    LEFT JOIN Personagem_Ataque pa ON p.id_player = pa.id_player
    GROUP BY p.id_player, p.nome_classe, p.level
    ORDER BY p.id_player
''')
personagens = cur.fetchall()

for id_player, classe, level, ataques in personagens:
    print(f'Personagem {id_player} ({classe}, Nível {level}): {ataques} ataques desbloqueados')

print('\n=== VERIFICAÇÃO: TODOS TÊM ATAQUE NÍVEL 1? ===')
cur.execute('''
    SELECT p.id_player, p.nome_classe, 
           CASE WHEN pa.id_ataque IS NOT NULL THEN 'SIM' ELSE 'NÃO' END as tem_ataque_nivel_1
    FROM Personagem p
    LEFT JOIN Personagem_Ataque pa ON p.id_player = pa.id_player
    LEFT JOIN Ataque_Especial ae ON pa.id_ataque = ae.id_ataque 
                                 AND ae.nivel_requerido = 1 
                                 AND ae.nome_classe = p.nome_classe
    ORDER BY p.id_player
''')
verificacao = cur.fetchall()

for id_player, classe, tem_ataque in verificacao:
    status = "✅" if tem_ataque == "SIM" else "❌"
    print(f'{status} Personagem {id_player} ({classe}): {tem_ataque}')

cur.close()
conn.close()
