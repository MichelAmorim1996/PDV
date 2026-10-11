from models import datetime, conectar


class RelatorioModel:
    @staticmethod
    def produtos_mais_vendidos(

        data_inicio,

        data_fim,

        limite=5

    ):

        with conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(

                """

                SELECT

                    p.nome,

                    SUM(iv.quantidade)

                    AS quantidade,

                    SUM(iv.total)

                    AS faturamento

                FROM itens_venda iv

                INNER JOIN produtos p

                    ON p.id = iv.id_produto

                INNER JOIN vendas v

                    ON v.id = iv.id_venda

                WHERE

                    date(v.data)

                    BETWEEN date(?)

                    AND date(?)

                    AND v.status = 'FINALIZADA'

                GROUP BY

                    iv.id_produto

                ORDER BY

                    quantidade DESC

                LIMIT ?

                """,

                (

                    data_inicio,

                    data_fim,

                    limite

                )

            )


            return cursor.fetchall()


    @staticmethod
    def resumo_periodo(

        data_inicio,

        data_fim

    ):

        with conectar() as conexao:

            cursor = conexao.cursor()


            cursor.execute(

                """

                SELECT

                    COUNT(*) AS quantidade_vendas,

                    COALESCE(

                        SUM(total),

                        0

                    ) AS faturamento

                FROM vendas

                WHERE

                    date(data)

                    BETWEEN date(?)

                    AND date(?)

                    AND status = 'FINALIZADA'

                """,

                (

                    data_inicio,

                    data_fim

                )

            )


            resumo = cursor.fetchone()


            quantidade = (

                resumo["quantidade_vendas"]

            )


            faturamento = (

                resumo["faturamento"]

            )


            ticket_medio = (

                faturamento / quantidade

                if quantidade > 0

                else 0

            )


            cursor.execute(

                """

                SELECT

                    forma_pagamento,

                    SUM(valor) AS total

                FROM pagamentos p

                INNER JOIN vendas v

                    ON v.id = p.id_venda

                WHERE

                    date(v.data)

                    BETWEEN date(?)

                    AND date(?)

                    AND v.status = 'FINALIZADA'

                GROUP BY forma_pagamento

                """,

                (

                    data_inicio,

                    data_fim

                )

            )


            pagamentos = {

                item["forma_pagamento"]:

                item["total"]

                for item in cursor.fetchall()

            }


            return {

                "quantidade_vendas":

                    quantidade,

                "faturamento":

                    faturamento,

                "ticket_medio":

                    ticket_medio,

                "pagamentos":

                    pagamentos

            }

    @staticmethod
    def ticket_medio():
        hoje = datetime.now().strftime("%Y-%m-%d")

        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(total), 0) AS total,
                    COUNT(*) AS quantidade
                FROM vendas
                WHERE date(data) = ?
                  AND status = 'FINALIZADA'
            """, (hoje,))
            resultado = cursor.fetchone()

            total = resultado["total"]
            quantidade = resultado["quantidade"]

            # Evitar divisão por zero
            if quantidade == 0:
                return 0.0

            return total / quantidade

    @staticmethod
    def vendas_hoje():

        hoje = datetime.now().strftime("%Y-%m-%d")

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """

                SELECT

                    COALESCE(

                        SUM(total),

                        0

                    ) AS total,

                    COUNT(*) AS quantidade

                FROM vendas

                WHERE

                    date(data) = ?

                    AND status = 'FINALIZADA'

                """,
                (hoje,),
            )

            resultado = cursor.fetchone()

            return {"total": resultado["total"], "quantidade": resultado["quantidade"]}


    @staticmethod
    def vendas_por_pagamento():

        hoje = datetime.now().strftime("%Y-%m-%d")

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """

                SELECT

                    forma_pagamento,

                    SUM(valor) AS total

                FROM pagamentos p

                INNER JOIN vendas v

                    ON v.id = p.id_venda

                WHERE

                    date(v.data) = ?

                    AND v.status = 'FINALIZADA'

                GROUP BY forma_pagamento

                """,
                (hoje,),
            )

            return cursor.fetchall()
