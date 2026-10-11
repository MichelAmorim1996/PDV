from models import conectar


class ProdutoModel:
    @staticmethod
    def cadastrar(
        codigo, nome, categoria, preco_custo, preco_venda, estoque, estoque_minimo
    ):
        with conectar() as conexao:
            cursor = conexao.cursor()

            cursor.execute(
                """
                INSERT INTO produtos (
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo,
                    ativo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """,
                (
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo,
                ),
            )

            conexao.commit()
            return cursor.lastrowid  # retorna o ID do novo produto

    @staticmethod
    def listar():
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT
                    id,
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo
                FROM produtos
                WHERE ativo = 1
                ORDER BY nome
            """)
            return cursor.fetchall()

    @staticmethod
    def buscar_por_id(produto_id):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo
                FROM produtos
                WHERE id = ?
            """,
                (produto_id,),
            )
            return cursor.fetchone()

    @staticmethod
    def buscar_por_nome(nome):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo
                FROM produtos
                WHERE ativo = 1
                  AND nome LIKE ?
                ORDER BY nome
            """,
                (f"%{nome}%",),
            )
            return cursor.fetchall()

    @staticmethod
    def atualizar(
        produto_id,
        codigo,
        nome,
        categoria,
        preco_custo,
        preco_venda,
        estoque,
        estoque_minimo,
    ):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                UPDATE produtos
                SET
                    codigo = ?,
                    nome = ?,
                    categoria = ?,
                    preco_custo = ?,
                    preco_venda = ?,
                    estoque = ?,
                    estoque_minimo = ?
                WHERE id = ?
            """,
                (
                    codigo,
                    nome,
                    categoria,
                    preco_custo,
                    preco_venda,
                    estoque,
                    estoque_minimo,
                    produto_id,
                ),
            )
            conexao.commit()

    @staticmethod
    def excluir(produto_id):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                UPDATE produtos
                SET ativo = 0
                WHERE id = ?
            """,
                (produto_id,),
            )
            conexao.commit()
