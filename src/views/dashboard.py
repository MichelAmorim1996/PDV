from views import ft, RelatorioController , RelatorioModel




@staticmethod
def ticket_medio():
    resultado = RelatorioModel.vendas_hoje()
    if resultado["quantidade"] == 0:

        return 0

    return resultado["total"] / resultado["quantidade"]


@ft.component
def Dashboard():

    vendas = RelatorioController.vendas_hoje()

    ticket = RelatorioController.ticket_medio()

    pagamentos = RelatorioController.vendas_por_pagamento()

    pagamentos_dict = {item["forma_pagamento"]: item["total"] for item in pagamentos}

    return ft.Column(
        [
            ft.Text("Dashboard", size=32, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Vendas hoje"),
                                    ft.Text(f"R$ " f"{vendas['total']:.2f}", size=24),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Quantidade"),
                                    ft.Text(str(vendas["quantidade"]), size=24),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Ticket médio"),
                                    ft.Text(f"R$ " f"{ticket:.2f}", size=24),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                ],
                wrap=True,
            ),
            ft.Divider(),
            ft.Text("Vendas por pagamento", size=22, weight=ft.FontWeight.BOLD),
            ft.Column(
                [
                    ft.Text(f"{forma}: " f"R$ {valor:.2f}")
                    for forma, valor in pagamentos_dict.items()
                ]
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
