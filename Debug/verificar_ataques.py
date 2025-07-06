import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='starwars_db',
    user='postgres',
    password='postgres',
    port='5432'
)
cur = conn.cursor()

print('=== ATAQUES ESPECIAIS POR CLASSE ===')
cur.execute('''
    SELECT nome_classe, nome_ataque, nivel_requerido, descricao, tipo_ataque
    FROM Ataque_Especial 
    ORDER BY nome_classe, nivel_requerido, nome_ataque
''')
ataques = cur.fetchall()

classe_atual = None
for classe, nome, nivel, desc, tipo in ataques:
    if classe != classe_atual:
        print(f'\n--- {classe} ---')
        classe_atual = classe
    print(f'  Nível {nivel}: {nome} ({tipo}) - {desc}')

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

cur.close()
conn.close()
