from components import ft


@ft.component
def ItemCarrinho(item, atualizar):

    def aumentar():

        from state import carrinho

        carrinho.aumentar(
            item["id"]
        )

        atualizar()


    def diminuir():

        from state import carrinho

        carrinho.diminuir(
            item["id"]
        )

        atualizar()


    def remover():

        from state import carrinho

        carrinho.remover(
            item["id"]
        )

        atualizar()


    return ft.Container(

        content=ft.Column(

            [

                ft.Text(

                    item["nome"],

                    size=16,

                    weight=ft.FontWeight.BOLD

                ),

                ft.Row(

                    [

                        ft.IconButton(

                            icon=ft.Icons.REMOVE,

                            on_click=diminuir

                        ),

                        ft.Text(

                            str(
                                item["quantidade"]
                            ),

                            size=16

                        ),

                        ft.IconButton(

                            icon=ft.Icons.ADD,

                            on_click=aumentar

                        ),

                        ft.Container(
                            expand=True
                        ),

                        ft.Text(

                            f"R$ "
                            f"{item['total']:.2f}",

                            size=16

                        ),

                        ft.IconButton(

                            icon=ft.Icons.DELETE,

                            on_click=remover

                        )

                    ]

                )

            ]

        ),

        padding=10,

        border=ft.Border.all(

            1,

            ft.Colors.OUTLINE

        ),

        border_radius=8,
        expand=True

    )