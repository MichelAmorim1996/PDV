from views import ft, ProdutoController


@ft.component
def EditarProduto():

    params = ft.use_route_params()

    produto_id = params["id"]

    produto = ProdutoController.buscar_por_id(produto_id)

    if not produto:

        return ft.Text("Produto não encontrado.")

    codigo, set_codigo = ft.use_state(produto["codigo"])

    nome, set_nome = ft.use_state(produto["nome"])

    categoria, set_categoria = ft.use_state(produto["categoria"])

    preco_custo, set_preco_custo = ft.use_state(str(produto["preco_custo"]))

    preco_venda, set_preco_venda = ft.use_state(str(produto["preco_venda"]))

    estoque, set_estoque = ft.use_state(str(produto["estoque"]))

    estoque_minimo, set_estoque_minimo = ft.use_state(str(produto["estoque_minimo"]))

    def salvar():

        ProdutoController.atualizar(
            produto_id,
            codigo,
            nome,
            categoria,
            float(preco_custo.replace(",", ".")),
            float(preco_venda.replace(",", ".")),
            float(estoque.replace(",", ".")),
            float(estoque_minimo.replace(",", ".")),
        )

        ft.context.page.navigate("/produtos")

    return ft.Column(
        [
            ft.Text("Editar Produto", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.TextField(
                label="Código",
                value=codigo,
                on_change=lambda e: set_codigo(e.control.value),
            ),
            ft.TextField(
                label="Nome", value=nome, on_change=lambda e: set_nome(e.control.value)
            ),
            ft.TextField(
                label="Categoria",
                value=categoria,
                on_change=lambda e: set_categoria(e.control.value),
            ),
            ft.TextField(
                label="Preço de custo",
                value=preco_custo,
                on_change=lambda e: set_preco_custo(e.control.value),
            ),
            ft.TextField(
                label="Preço de venda",
                value=preco_venda,
                on_change=lambda e: set_preco_venda(e.control.value),
            ),
            ft.TextField(
                label="Estoque",
                value=estoque,
                on_change=lambda e: set_estoque(e.control.value),
            ),
            ft.TextField(
                label="Estoque mínimo",
                value=estoque_minimo,
                on_change=lambda e: set_estoque_minimo(e.control.value),
            ),
            ft.Row(
                [
                    ft.Button(
                        "Cancelar",
                        on_click=lambda: ft.context.page.navigate("/produtos"),
                    ),
                    ft.Button("Salvar", on_click=salvar),
                ]
            ),
        ]
    )
