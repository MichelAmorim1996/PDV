from views import ft, CaixaController


@ft.component
def Caixa():
    caixa = CaixaController.caixa_aberto()
    historico = CaixaController.historico()

    movimentacoes_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Valor")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Data")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(m["tipo"])),
                    ft.DataCell(ft.Text(f"R$ {m['valor']:.2f}")),
                    ft.DataCell(ft.Text(m["descricao"] or "")),
                    ft.DataCell(ft.Text(m["data"])),
                ]
            )
            for m in historico
        ],
    )




    if not caixa:
        return ft.Column(
            [
                ft.Text("Nenhum caixa aberto", size=28, weight=ft.FontWeight.BOLD),
                ft.Text("Abra um caixa para iniciar as operações."),
                ft.Button(
                    "Abrir caixa",
                    icon=ft.Icons.LOCK_OPEN,
                    on_click=lambda: ft.context.page.navigate("/caixa/abrir"),
                ),
            ],
            spacing=20,
        )

    # Só chama saldo_atual se o caixa estiver aberto
    saldo = CaixaController.saldo_atual()

    return ft.Column(
        [
            ft.Text("Caixa Aberto", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row(
                [
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Valor inicial"),
                                    ft.Text(f"R$ {caixa['valor_inicial']:.2f}", size=22),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Status"),
                                    ft.Text("ABERTO", size=22),
                                ]
                            ),
                            padding=20,
                        )
                    ),
                ]
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Saldo atual"),
                            ft.Text(f"R$ {saldo:.2f}", size=22, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    padding=20,
                )
            ),
        ft.Divider(),
        ft.Text("Histórico de movimentações", size=20, weight=ft.FontWeight.BOLD),
        movimentacoes_table,
        ft.Row(
            [
                ft.Button("Suprimento", icon=ft.Icons.ADD, on_click=lambda: ft.context.page.navigate("/caixa/suprimento")),
                ft.Button("Sangria", icon=ft.Icons.REMOVE, on_click=lambda: ft.context.page.navigate("/caixa/sangria")),
                ft.Button("Fechar caixa", icon=ft.Icons.LOCK, on_click=lambda: ft.context.page.navigate("/caixa/fechar")),
            ]
        ),


        ],
        spacing=20,
        height=ft.context.page.height-100,
        scroll=ft.ScrollMode.AUTO
    )
