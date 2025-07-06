import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database='starwars_db',
    user='postgres',
    password='postgres',
    port='5432'
)
cur = conn.cursor()

print('=== PLANETAS SEM CIDADES ===')
cur.execute('''
    SELECT p.nome_planeta 
    FROM Planeta p 
    LEFT JOIN Cidade c ON p.nome_planeta = c.nome_planeta 
    WHERE c.nome_planeta IS NULL
    ORDER BY p.nome_planeta
''')
planetas_sem_cidades = cur.fetchall()
for planeta in planetas_sem_cidades:
    print(f'- {planeta[0]}')

print('\n=== PLANETAS COM CIDADES ===')
cur.execute('''
    SELECT p.nome_planeta, COUNT(c.id_cidade) as total_cidades
    FROM Planeta p 
    LEFT JOIN Cidade c ON p.nome_planeta = c.nome_planeta 
    GROUP BY p.nome_planeta
    HAVING COUNT(c.id_cidade) > 0
    ORDER BY total_cidades DESC, p.nome_planeta
''')
planetas_com_cidades = cur.fetchall()
for planeta, total in planetas_com_cidades:
    print(f'- {planeta}: {total} cidades')

print('\n=== CLASSES EXISTENTES ===')
cur.execute('SELECT nome_classe FROM Classe ORDER BY nome_classe')
classes = cur.fetchall()
for classe in classes:
    print(f'- {classe[0]}')

print('\n=== TODOS OS PLANETAS ===')
cur.execute('SELECT nome_planeta FROM Planeta ORDER BY nome_planeta')
todos_planetas = cur.fetchall()
for planeta in todos_planetas:
    print(f'- {planeta[0]}')

cur.close()
conn.close()
