from controllers import EstoqueModel


class EstoqueController:

    @staticmethod
    def entrada(id_produto, quantidade, motivo):

        if quantidade <= 0:

            raise ValueError("A quantidade deve ser maior que zero.")

        EstoqueModel.movimentar(id_produto, quantidade, "ENTRADA", motivo)

    @staticmethod
    def ajuste(id_produto, quantidade, motivo):

        EstoqueModel.movimentar(id_produto, quantidade, "AJUSTE", motivo)
