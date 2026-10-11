from controllers import ImpressoraService, time


class ImpressoraController:

    @staticmethod
    def imprimir_venda(venda, itens):

        impressora = None

        try:

            impressora = ImpressoraService()

            impressora.imprimir_cupom(

                venda,

                itens

            )

            time.sleep(0.5)

        finally:

            if impressora:

                impressora.fechar()