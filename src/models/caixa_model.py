from models import datetime, conectar


class CaixaModel:
    @staticmethod
    def historico_movimentacoes(id_caixa):
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                SELECT tipo, valor, descricao, data
                FROM movimentacoes_caixa
                WHERE id_caixa = ?
                ORDER BY data DESC
                """,
                (id_caixa,),
            )
            return cursor.fetchall()

    @staticmethod
    def fechar_caixa(id_caixa, valor_contado):

        conexao = conectar()

        cursor = conexao.cursor()

        try:

            # Buscar caixa

            cursor.execute(
                """

                SELECT *

                FROM caixas

                WHERE id = ?

                AND status = 'ABERTO'

                """,
                (id_caixa,),
            )

            caixa = cursor.fetchone()

            if not caixa:

                raise ValueError("Caixa aberto não encontrado.")

            # Calcular movimentações

            cursor.execute(
                """

                SELECT

                    COALESCE(

                        SUM(

                            CASE

                                WHEN tipo IN (

                                    'VENDA',

                                    'SUPRIMENTO'

                                )

                                THEN valor


                                WHEN tipo IN (

                                    'SANGRIA',

                                    'ESTORNO'

                                )

                                THEN -valor


                                ELSE 0

                            END

                        ),

                        0

                    ) AS movimentacoes

                FROM movimentacoes_caixa

                WHERE id_caixa = ?

                """,
                (id_caixa,),
            )

            movimentacoes = cursor.fetchone()["movimentacoes"]

            valor_esperado = caixa["valor_inicial"] + movimentacoes

            diferenca = valor_contado - valor_esperado

            # Atualizar caixa

            cursor.execute(
                """

                UPDATE caixas

                SET

                    status = 'FECHADO',

                    data_fechamento =

                        CURRENT_TIMESTAMP,

                    valor_final = ?,

                    valor_esperado = ?,

                    diferenca = ?

                WHERE id = ?

                """,
                (valor_contado, valor_esperado, diferenca, id_caixa),
            )

            conexao.commit()

            return {
                "valor_esperado": valor_esperado,
                "valor_contado": valor_contado,
                "diferenca": diferenca,
            }

        except Exception:

            conexao.rollback()

            raise

        finally:

            conexao.close()

    @staticmethod
    def resumo_caixa(id_caixa):

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT

                    c.valor_inicial,

                    COALESCE(

                        SUM(

                            CASE
                            
                                    WHEN m.tipo IN (
                                        'VENDA',
                                        'SUPRIMENTO'
                                    )
                            
                                    THEN m.valor
                            
                            
                                    WHEN m.tipo IN (
                                        'SANGRIA',
                                        'ESTORNO'
                                    )
                            
                                    THEN -m.valor
                            
                            
                                    ELSE 0
                            
                                END

                        ),

                        0

                    ) AS vendas,

                    COALESCE(

                        SUM(

                            CASE

                                WHEN m.tipo = 'SUPRIMENTO'
                                THEN m.valor

                                ELSE 0

                            END

                        ),

                        0

                    ) AS suprimentos,

                    COALESCE(

                        SUM(

                            CASE

                                WHEN m.tipo = 'SANGRIA'
                                THEN m.valor

                                ELSE 0

                            END

                        ),

                        0

                    ) AS sangrias

                FROM caixas c

                LEFT JOIN movimentacoes_caixa m

                    ON m.id_caixa = c.id

                WHERE c.id = ?

                GROUP BY

                    c.id,

                    c.valor_inicial

            """,
                (id_caixa,),
            )

            resumo = cursor.fetchone()

            if not resumo:

                return None

            saldo_esperado = (
                resumo["valor_inicial"]
                + resumo["vendas"]
                + resumo["suprimentos"]
                - resumo["sangrias"]
            )

            return {
                "valor_inicial": resumo["valor_inicial"],
                "vendas": resumo["vendas"],
                "suprimentos": resumo["suprimentos"],
                "sangrias": resumo["sangrias"],
                "saldo_esperado": saldo_esperado,
            }

    @staticmethod
    def sangria(id_caixa, valor, descricao):

        with conectar() as conexao:

            cursor = conexao.cursor()

            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO movimentacoes_caixa (

                    id_caixa,
                    tipo,
                    valor,
                    descricao,
                    data

                )

                VALUES (?, ?, ?, ?, ?)
            """,
                (id_caixa, "SANGRIA", valor, descricao, data),
            )

            conexao.commit()

    @staticmethod
    def suprimento(id_caixa, valor, descricao):

        with conectar() as conexao:

            cursor = conexao.cursor()

            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO movimentacoes_caixa (

                    id_caixa,
                    tipo,
                    valor,
                    descricao,
                    data

                )

                VALUES (?, ?, ?, ?, ?)
            """,
                (id_caixa, "SUPRIMENTO", valor, descricao, data),
            )

            conexao.commit()

    @staticmethod
    def calcular_saldo(id_caixa):

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT valor_inicial

                FROM caixas

                WHERE id = ?
            """,
                (id_caixa,),
            )

            caixa = cursor.fetchone()

            if not caixa:

                return 0

            saldo = caixa["valor_inicial"]

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(
                        CASE
                            WHEN tipo IN ('VENDA', 'SUPRIMENTO')
                            THEN valor
                            WHEN tipo = 'SANGRIA'
                            THEN -valor
                            ELSE 0
                        END
                    ), 0) AS total

                FROM movimentacoes_caixa

                WHERE id_caixa = ?
            """,
                (id_caixa,),
            )

            movimentacoes = cursor.fetchone()

            return saldo + movimentacoes["total"]

    @staticmethod
    def registrar_movimentacao(id_caixa, tipo, valor, descricao=""):

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute(
                """

                INSERT INTO movimentacoes_caixa (

                    id_caixa,

                    tipo,

                    valor,

                    descricao,

                    data

                )

                VALUES (?, ?, ?, ?, ?)

                """,
                (id_caixa, tipo, valor, descricao, data),
            )

        conexao.commit()

    @staticmethod
    def buscar_caixa_aberto():

        with conectar() as conexao:

            cursor = conexao.cursor()

            cursor.execute("""
                SELECT *

                FROM caixas

                WHERE status = 'ABERTO'

                ORDER BY id DESC

                LIMIT 1
            """)

            return cursor.fetchone()

    @staticmethod
    def abrir(valor_inicial):

        with conectar() as conexao:

            cursor = conexao.cursor()

            caixa_aberto = CaixaModel.buscar_caixa_aberto()

            if caixa_aberto:

                raise ValueError("Já existe um caixa aberto.")

            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO caixas (

                    data_abertura,

                    valor_inicial,

                    status

                )

                VALUES (?, ?, ?)
            """,
                (data, valor_inicial, "ABERTO"),
            )

            conexao.commit()

            return cursor.lastrowid
