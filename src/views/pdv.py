from views import ft, ProdutoController, CardProdutoPDV, PainelCarrinho


@ft.component
def PDV():

    produtos, set_produtos = ft.use_state(ProdutoController.listar())

    contador, set_contador = ft.use_state(0)

    def atualizar_carrinho():

        set_contador(contador + 1)

    def pesquisar(e):

        resultado = ProdutoController.buscar(e.control.value)

        set_produtos(resultado)

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Produtos", size=28, weight=ft.FontWeight.BOLD),
                                ft.TextField(
                                    label="Pesquisar produto",
                                    prefix_icon=ft.Icons.SEARCH,
                                    on_change=pesquisar,
                                ),
                                ft.GridView(
                                    expand=True,
                                    max_extent=240,
                                    spacing=16,
                                    run_spacing=16,
                                    controls=[
                                        CardProdutoPDV(produto, atualizar_carrinho)
                                        for produto in produtos
                                    ],
                                    height=ft.context.page.height - 300,
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                            ],
                            expand=True,
                        ),
                        expand=True,
                        padding=20,
                    ),
                    ft.VerticalDivider(),
                    ft.Container(
                        content=PainelCarrinho(),
                        width=400,
                        padding=20,
                    ),
                ],
                expand=True,
            )
        ],
        expand=True,
    )
