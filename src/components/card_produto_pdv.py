from components import ft, carrinho




@ft.component
def CardProdutoPDV(produto, atualizar_carrinho):

    def adicionar():

        carrinho.adicionar(
            produto
        )

        atualizar_carrinho()


    return ft.Card(

        content=ft.Container(

            content=ft.Column(

                [

                    ft.Text(

                        produto["nome"],

                        size=18,

                        weight=ft.FontWeight.BOLD

                    ),

                    ft.Text(

                        produto["categoria"]

                    ),

                    ft.Text(

                        f"R$ "
                        f"{produto['preco_venda']:.2f}",

                        size=20,

                        weight=ft.FontWeight.BOLD

                    ),

                    ft.Icon(
                        
                        icon=ft.Icons.ADD_SHOPPING_CART,
                        color=ft.Colors.BLUE_400,

                    )

                ],

                spacing=8

            ),
        

            padding=16,
            on_click=adicionar,
            ink=True
            
            

        )

    )