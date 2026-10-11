from components import ft, ProdutoController



@ft.component
def CardProduto(produto, ao_excluir=None):



    def editar():

        ft.context.page.navigate(

            f"/produtos/editar/{produto['id']}"

        )


    def excluir():

        ProdutoController.excluir(

            produto["id"]

        )

        if ao_excluir:

            ao_excluir(

                produto["id"]

            )


    def fechar_dialog(e=None):

        ft.context.page.pop_dialog()


    def abrir_dialog_exclusao(e=None):

        campo_confirmacao = ft.TextField(

            label="Digite DELETE",

            autofocus=True

        )


        def confirmar_exclusao(e=None):

            texto = (

                campo_confirmacao.value

                or ""

            ).strip().upper()


            if texto != "DELETE":

                campo_confirmacao.error_text = (

                    "Digite DELETE para confirmar."

                )

                campo_confirmacao.update()

                return


            fechar_dialog()

            excluir()


        dialog = ft.AlertDialog(

            modal=True,

            title=ft.Text(

                "Excluir produto?"

            ),

            content=ft.Column(

                [

                    ft.Text(

                        "Esta ação é permanente "

                        "e não pode ser desfeita."

                    ),

                    ft.Text(

                        "Digite DELETE para confirmar:"

                    ),

                    campo_confirmacao

                ],

                tight=True,

                spacing=15

            ),

            actions=[

                ft.TextButton(

                    content="Cancelar",

                    on_click=fechar_dialog

                ),

                ft.Button(

                    content="Excluir definitivamente",

                    icon=ft.Icons.DELETE_FOREVER,

                    on_click=confirmar_exclusao

                )

            ],

            actions_alignment=

            ft.MainAxisAlignment.END

        )


        ft.context.page.show_dialog(

            dialog

        )


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

                        f"Categoria: "

                        f"{produto['categoria']}"

                    ),

                    ft.Text(

                        f"Código: "

                        f"{produto['codigo']}"

                    ),

                    ft.Text(

                        f"Estoque: "

                        f"{produto['estoque']}"

                    ),

                    ft.Text(

                        f"R$ "

                        f"{produto['preco_venda']:.2f}",

                        size=20,

                        weight=ft.FontWeight.BOLD

                    ),

                    ft.Row(

                        [

                            

                            ft.Button(

                                "Excluir",

                                icon=ft.Icons.DELETE,

                                on_click=

                                abrir_dialog_exclusao

                            )

                        ]

                    )

                ],

                spacing=8,
                height=

                ft.context.page.height - 100,

                scroll=
                ft.ScrollMode.AUTO,

                expand=True

            ),

            padding=16,
            ink=True,
            on_click=editar

        )

    )