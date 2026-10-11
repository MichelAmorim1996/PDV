from controllers import CaixaModel


class CaixaController:
    @staticmethod
    def historico():
        caixa = CaixaModel.buscar_caixa_aberto()
        if not caixa:
            return []
        return CaixaModel.historico_movimentacoes(caixa["id"])




    @staticmethod
    def fechar_caixa(

        id_caixa,

        valor_contado

    ):

        if valor_contado < 0:

            raise ValueError(

                "Valor inválido."

            )


        return CaixaModel.fechar_caixa(

            id_caixa,

            valor_contado

        )





    @staticmethod
    def resumo_caixa():

        caixa = CaixaModel.buscar_caixa_aberto()


        if not caixa:

            raise ValueError(

                "Não existe caixa aberto."

            )


        return CaixaModel.resumo_caixa(

            caixa["id"]

        )






    @staticmethod
    def suprimento(
        valor,
        descricao
    ):

        caixa = CaixaModel.buscar_caixa_aberto()

        if not caixa:

            raise ValueError(
                "Não existe caixa aberto."
            )


        if valor <= 0:

            raise ValueError(
                "O valor deve ser maior que zero."
            )


        CaixaModel.suprimento(

            caixa["id"],

            valor,

            descricao

        )



    @staticmethod
    def sangria(
        valor,
        descricao
    ):

        caixa = CaixaModel.buscar_caixa_aberto()

        if not caixa:

            raise ValueError(
                "Não existe caixa aberto."
            )


        if valor <= 0:

            raise ValueError(
                "O valor deve ser maior que zero."
            )


        saldo = CaixaModel.calcular_saldo(

            caixa["id"]

        )


        if valor > saldo:

            raise ValueError(

                f"Saldo insuficiente. "
                f"Disponível: R$ {saldo:.2f}"

            )


        CaixaModel.sangria(

            caixa["id"],

            valor,

            descricao

    )



    @staticmethod
    def saldo_atual():

        caixa = CaixaModel.buscar_caixa_aberto()

        if not caixa:

            raise ValueError(
                "Não existe caixa aberto."
            )

        return CaixaModel.calcular_saldo(
            caixa["id"]
    )


    @staticmethod
    def caixa_aberto():

        return CaixaModel.buscar_caixa_aberto()


    @staticmethod
    def abrir(valor_inicial):

        if valor_inicial < 0:

            raise ValueError(
                "O valor inicial não pode ser negativo."
            )

        return CaixaModel.abrir(
            valor_inicial
        )