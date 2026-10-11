from models import datetime


class EstoqueModel:

    @staticmethod
    def movimentar(cursor, id_produto, quantidade, tipo, motivo=""):

        cursor.execute(
            """

            SELECT estoque

            FROM produtos

            WHERE id = ?

            """,
            (id_produto,),
        )

        produto = cursor.fetchone()

        if not produto:

            raise ValueError("Produto não encontrado.")

        estoque_anterior = produto["estoque"]

        if tipo in ("ENTRADA", "CANCELAMENTO"):

            estoque_posterior = estoque_anterior + quantidade

        elif tipo in ("VENDA", "SAIDA"):

            estoque_posterior = estoque_anterior - quantidade

        else:

            raise ValueError("Tipo de movimentação inválido.")

        if estoque_posterior < 0:

            raise ValueError("Estoque insuficiente.")

        cursor.execute(
            """

            UPDATE produtos

            SET estoque = ?

            WHERE id = ?

            """,
            (estoque_posterior, id_produto),
        )

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            """

            INSERT INTO

            movimentacoes_estoque (

                id_produto,

                tipo,

                quantidade,

                estoque_anterior,

                estoque_posterior,

                motivo,

                data

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

            """,
            (
                id_produto,
                tipo,
                quantidade,
                estoque_anterior,
                estoque_posterior,
                motivo,
                data,
            ),
        )
