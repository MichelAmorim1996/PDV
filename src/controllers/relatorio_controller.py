from controllers import RelatorioModel


class RelatorioController:

    @staticmethod
    def vendas_hoje():

        return (

            RelatorioModel.vendas_hoje()

        )


    @staticmethod
    def ticket_medio():

        return (

            RelatorioModel.ticket_medio()

        )


    @staticmethod
    def vendas_por_pagamento():

        return (

            RelatorioModel.vendas_por_pagamento()

        )