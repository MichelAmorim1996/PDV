from views import ft, VendaController


@ft.component
def Vendas():

    vendas = VendaController.listar_vendas()

    if not vendas:

        return ft.Column([ft.Text("Nenhuma venda realizada.", size=24)])

    lista = []

    for venda in vendas:

        lista.append(
            ft.Card(
                content=ft.ListTile(
                    title=ft.Text(f"Venda #{venda['id']}"),
                    subtitle=ft.Text(venda["data"]),
                    trailing=ft.Column(
                        [
                            ft.Text(f"R$ " f"{venda['total']:.2f}"),
                            ft.Text(venda["forma_pagamento"]),
                        ]
                    ),
                    on_click=lambda e, id_venda=venda["id"]: ft.context.page.navigate(
                        f"/vendas/{id_venda}"
                    ),
                )
            )
        )

    return ft.Column(
        [
            ft.Text("Histórico de Vendas", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ListView(controls=lista, expand=True),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        height=ft.context.page.height - 100,
    )
