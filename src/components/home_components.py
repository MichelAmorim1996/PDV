from components import ft


@ft.component
def BotaoAcao(
    titulo,
    icone,
    rota
):

    def navegar(e):
        ft.context.page.navigate(rota)

    return ft.Card(
        width=220,
        height=120,
        content=ft.Container(
            padding=20,
            on_click=navegar,
            content=ft.Column(
                [
                    ft.Icon(
                        icone,
                        size=40
                    ),

                    ft.Text(
                        titulo,
                        size=18,
                        weight=ft.FontWeight.BOLD
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
    )