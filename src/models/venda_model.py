from models import (
    datetime,
    conectar,
    EstoqueInsuficienteError,
    VendaCanceladaError,
    EstoqueModel,
)


class VendaModel:

    @staticmethod
    def registrar_venda(id_caixa, itens, forma_pagamento, total):

        conexao = conectar()

        cursor = conexao.cursor()

        try:

            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # =========================
            # 1. REGISTRAR VENDA
            # =========================

            cursor.execute(
                """

                INSERT INTO vendas (

                    id_caixa,

                    data,

                    subtotal,

                    desconto,

                    acrescimo,

                    total,

                    status

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)

                """,
                (id_caixa, data, total, 0, 0, total, "FINALIZADA"),
            )

            id_venda = cursor.lastrowid

            # =========================
            # 2. REGISTRAR ITENS
            # =========================

            for item in itens:

                cursor.execute(
                    """

                    INSERT INTO itens_venda (

                        id_venda,

                        id_produto,

                        quantidade,

                        preco_unitario,

                        total

                    )

                    VALUES (?, ?, ?, ?, ?)

                    """,
                    (
                        id_venda,
                        item["id"],
                        item["quantidade"],
                        item["preco_unitario"],
                        item["total"],
                    ),
                )

                # =====================
                # 3. BAIXAR ESTOQUE
                # =====================

                EstoqueModel.movimentar(
                    cursor,
                    item["id"],
                    item["quantidade"],
                    "VENDA",
                    f"Venda #{id_venda}",
                )

            # =========================
            # 4. REGISTRAR PAGAMENTO
            # =========================

            cursor.execute(
                """

                INSERT INTO pagamentos (

                    id_venda,

                    forma_pagamento,

                    valor

                )

                VALUES (?, ?, ?)

                """,
                (id_venda, forma_pagamento, total),
            )

            # =========================
            # 5. MOVIMENTAÇÃO DO CAIXA
            # =========================

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
                (id_caixa, "VENDA", total, f"Venda #{id_venda}", data),
            )

            conexao.commit()

            return id_venda

        except Exception:

            conexao.rollback()

            raise

        finally:

            conexao.close()

    @staticmethod
    def buscar_venda(id_venda):
        with conectar() as conexao:
            cursor = conexao.cursor()

            # Buscar dados principais da venda
            cursor.execute(
                """
                SELECT
                    v.id,
                    v.id_caixa,
                    v.data,
                    v.subtotal,
                    v.desconto,
                    v.acrescimo,
                    v.total,
                    v.status,
                    p.forma_pagamento,
                    p.valor AS valor_pago
                FROM vendas v
                LEFT JOIN pagamentos p
                    ON p.id_venda = v.id
                WHERE v.id = ?
            """,
                (id_venda,),
            )
            venda = cursor.fetchone()

            if not venda:
                return None

            # Buscar itens da venda
            cursor.execute(
                """
                SELECT
                    iv.id_produto,
                    iv.quantidade,
                    iv.preco_unitario,
                    iv.total,
                    pr.nome
                FROM itens_venda iv
                INNER JOIN produtos pr
                    ON pr.id = iv.id_produto
                WHERE iv.id_venda = ?
            """,
                (id_venda,),
            )
            itens = cursor.fetchall()

            return {"venda": venda, "itens": itens}

    @staticmethod
    def listar_vendas():
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT
                    v.id,
                    v.data,
                    v.total,
                    v.status,
                    p.forma_pagamento
                FROM vendas v
                LEFT JOIN pagamentos p
                    ON p.id_venda = v.id
                ORDER BY v.id DESC
            """)
            return cursor.fetchall()

    @staticmethod
    def cancelar_venda(id_venda):
        with conectar() as conexao:
            cursor = conexao.cursor()
            try:
                # 1. Buscar a venda
                cursor.execute(
                    """
                    SELECT id, id_caixa, total, status
                    FROM vendas
                    WHERE id = ?
                """,
                    (id_venda,),
                )
                venda = cursor.fetchone()

                if not venda:
                    raise ValueError("Venda não encontrada.")

                if venda["status"] == "CANCELADA":
                    raise VendaCanceladaError("Esta venda já foi cancelada.")

                # 2. Buscar os itens
                cursor.execute(
                    """
                    SELECT id_produto, quantidade
                    FROM itens_venda
                    WHERE id_venda = ?
                """,
                    (id_venda,),
                )
                itens = cursor.fetchall()

                # 3. Devolver estoque
                for item in itens:
                    cursor.execute(
                        """
                        UPDATE produtos
                        SET estoque = estoque + ?
                        WHERE id = ?
                    """,
                        (item["quantidade"], item["id_produto"]),
                    )

                # 4. Alterar status da venda
                cursor.execute(
                    """
                    UPDATE vendas
                    SET status = 'CANCELADA'
                    WHERE id = ?
                """,
                    (id_venda,),
                )

                # 5. Registrar estorno no caixa
                data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    """
                    INSERT INTO movimentacoes_caixa (
                        id_caixa, tipo, valor, descricao, data
                    )
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        venda["id_caixa"],
                        "ESTORNO",
                        venda["total"],
                        f"Estorno da venda #{id_venda}",
                        data,
                    ),
                )

                conexao.commit()
            except Exception:
                conexao.rollback()
                raise
