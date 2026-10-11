from components import ft, carrinho, ItemCarrinho


@ft.component
def PainelCarrinho():
    contador, set_contador = ft.use_state(0)

    def atualizar():
        set_contador(contador + 1)

    itens = carrinho.itens

    return ft.Column(
        [
            ft.Text("Carrinho", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            # Lista de itens com scroll
            ft.Column(
                [
                    ItemCarrinho(item, atualizar)
                    for item in itens
                ],
                height=ft.context.page.height - 500,
                scroll=ft.ScrollMode.AUTO,   # scroll aqui
                expand=True                  # ocupa espaço disponível
            ),

            ft.Divider(),
            ft.Row(
                [
                    ft.Text("Total:", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Text(
                        f"R$ {carrinho.total():.2f}",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    )
                ]
            ),
            ft.Button(
                "Finalizar Venda",
                icon=ft.Icons.PAYMENT,
                expand=True,
                on_click=lambda: ft.context.page.navigate("/pagamento")
            )
        ],
        expand=True
    )
