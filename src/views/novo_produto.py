from views import ft, ProdutoController


@ft.component
def NovoProduto():

    codigo, set_codigo = ft.use_state("")
    nome, set_nome = ft.use_state("")
    categoria, set_categoria = ft.use_state("Categoria")
    preco_custo, set_preco_custo = ft.use_state("")
    preco_venda, set_preco_venda = ft.use_state("")
    estoque, set_estoque = ft.use_state("")
    estoque_minimo, set_estoque_minimo = ft.use_state("")

    mensagem, set_mensagem = ft.use_state("")

    def salvar_produto():

        if not codigo.strip():
            set_mensagem("Informe o código do produto.")
            return

        if not nome.strip():
            set_mensagem("Informe o nome do produto.")
            return

        if not categoria.strip():
            set_mensagem("Informe a categoria.")
            return

        try:

            valor_custo = float(preco_custo.replace(",", ".") or 0)

            valor_venda = float(preco_venda.replace(",", "."))

            quantidade_estoque = float(estoque.replace(",", ".") or 0)

            quantidade_minima = float(estoque_minimo.replace(",", ".") or 0)

        except ValueError:

            set_mensagem("Informe valores numéricos válidos.")

            return

        ProdutoController.cadastrar(
            codigo=codigo,
            nome=nome,
            categoria=categoria,
            preco_custo=valor_custo,
            preco_venda=valor_venda,
            estoque=quantidade_estoque,
            estoque_minimo=quantidade_minima,
        )

        ft.context.page.navigate("/produtos")

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Novo Produto", size=28, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.Button(
                        "Voltar", on_click=lambda: ft.context.page.navigate("/produtos")
                    ),
                ]
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.TextField(
                            label="Código",
                            value=codigo,
                            on_change=lambda e: set_codigo(e.control.value),
                        ),
                        ft.TextField(
                            label="Nome do produto",
                            value=nome,
                            on_change=lambda e: set_nome(e.control.value),
                        ),
                        ft.Dropdown(
                            label="Categoria",
                            value=categoria,
                            options=[
                                ft.DropdownOption("Bolos"),
                                ft.DropdownOption("Bebidas"),
                                ft.DropdownOption("Doces"),
                                ft.DropdownOption("Aperitivos"),
                            ],
                            on_select=lambda e: set_categoria(e.control.value),
                        ),
                        ft.Row(
                            [
                                ft.TextField(
                                    label="Preço de custo",
                                    value=preco_custo,
                                    expand=True,
                                    on_change=lambda e: set_preco_custo(
                                        e.control.value
                                    ),
                                ),
                                ft.TextField(
                                    label="Preço de venda",
                                    value=preco_venda,
                                    expand=True,
                                    on_change=lambda e: set_preco_venda(
                                        e.control.value
                                    ),
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.TextField(
                                    label="Estoque inicial",
                                    value=estoque,
                                    expand=True,
                                    on_change=lambda e: set_estoque(e.control.value),
                                ),
                                ft.TextField(
                                    label="Estoque mínimo",
                                    value=estoque_minimo,
                                    expand=True,
                                    on_change=lambda e: set_estoque_minimo(
                                        e.control.value
                                    ),
                                ),
                            ]
                        ),
                        ft.Text(mensagem, color=ft.Colors.RED),
                        ft.Row(
                            [
                                ft.Button(
                                    "Cancelar",
                                    on_click=lambda: ft.context.page.navigate(
                                        "/produtos"
                                    ),
                                ),
                                ft.Button("Salvar produto", on_click=salvar_produto),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=20,
                ),
                width=600,
                padding=30,
            ),
        ],
        expand=True,
        height=ft.context.page.height - 100,
        scroll=ft.ScrollMode.AUTO,  # scroll aqui
    )
