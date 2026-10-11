from controllers import VendaModel

from controllers.caixa_controller import CaixaController


class VendaController:
    @staticmethod
    def cancelar_venda(id_venda):

        return VendaModel.cancelar_venda(id_venda)

    @staticmethod
    def buscar_venda(id_venda):

        return VendaModel.buscar_venda(id_venda)

    @staticmethod
    def listar_vendas():

        return VendaModel.listar_vendas()

    @staticmethod
    def finalizar_venda(itens, forma_pagamento):

        if not itens:

            raise ValueError("O carrinho está vazio.")

        caixa = CaixaController.caixa_aberto()

        if not caixa:

            raise ValueError("Não existe um caixa aberto.")

        total = sum(item["total"] for item in itens)

        return VendaModel.registrar_venda(caixa["id"], itens, forma_pagamento, total)
