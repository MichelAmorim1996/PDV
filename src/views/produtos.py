from views import ft, ProdutoController, CardProduto




@ft.component
def Produtos():

    produtos, set_produtos = ft.use_state(
        ProdutoController.listar()
    )

    def remover_produto_da_lista(id_produto):

        set_produtos(

            [

                produto

                for produto in produtos

                if produto["id"] != id_produto

            ]

    )

    

    pesquisa, set_pesquisa = ft.use_state("")


    def pesquisar(e):

        set_pesquisa = ProdutoController.buscar(
            e.control.value
        )

        set_produtos(set_pesquisa)


    return ft.Column(

        [

            ft.Row(

                [

                    ft.Text(
                        "Produtos",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(
                        expand=True
                    ),

                    ft.Button(
                        "Novo Produto",
                        on_click=lambda:
                            ft.context.page.navigate(
                                "/produtos/novo"
                            )
                    )

                ]

            ),

            ft.TextField(

                label="Pesquisar produto",
                value=pesquisa,

                prefix_icon=ft.Icons.SEARCH,

                on_change=pesquisar

            ),

            ft.Divider(),
            #ft.Text(str(produtos)),

            ft.GridView(

                expand=True,

                max_extent=280,

                spacing=16,

                run_spacing=16,

                controls=[

                    CardProduto(produto, ao_excluir=remover_produto_da_lista) for produto in produtos

                    

                ]

            )

        ],

        expand=True,
        height=ft.context.page.height-100,
        scroll=ft.ScrollMode.AUTO

    )