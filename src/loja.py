import psycopg2
from psycopg2.extensions import connection as _Connection

class Produto:
    def __init__(self, id, nome, descricao, preco, estoque):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque

class Loja:
    def __init__(self, conexao: _Connection):
        self.conn = conexao

    def listar_produtos(self) -> list[Produto]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, nome, descricao, preco, quantidade_estoque
            FROM produto
        """)
        rows = cur.fetchall()
        cur.close()
        return [Produto(*r) for r in rows]

    def comprar(self, personagem_id: int) -> bool:
        cur = self.conn.cursor()
        try:
            # Bloqueia o personagem para ler saldo
            cur.execute(
                "SELECT saldo FROM personagem WHERE id = %s FOR UPDATE",
                (personagem_id,)
            )
            row = cur.fetchone()
            if not row:
                return False
            saldo = row[0]

            # Escolha de produto por ID
            prod_id = int(input("Digite o ID do produto que deseja comprar: "))
            cur.execute(
                "SELECT preco, quantidade_estoque FROM produto WHERE id = %s FOR UPDATE",
                (prod_id,)
            )
            produto = cur.fetchone()
            if not produto:
                return False
            preco, estoque = produto

            # Verifica saldo e estoque
            if preco > saldo or (estoque is not None and estoque <= 0):
                return False

            # Atualiza saldo do personagem
            cur.execute(
                "UPDATE personagem SET saldo = saldo - %s WHERE id = %s",
                (preco, personagem_id)
            )

            # Atualiza estoque do produto (se limitado)
            if estoque is not None:
                cur.execute(
                    "UPDATE produto SET quantidade_estoque = quantidade_estoque - 1 WHERE id = %s",
                    (prod_id,)
                )

            # Insere ou incrementa em personagem_produto
            cur.execute("""
                INSERT INTO personagem_produto (personagem_id, produto_id, quantidade)
                VALUES (%s, %s, 1)
                ON CONFLICT (personagem_id, produto_id) DO
                  UPDATE SET quantidade = personagem_produto.quantidade + 1
            """, (personagem_id, prod_id))

            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False
        finally:
            cur.close()
