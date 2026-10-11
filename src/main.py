from src import *


def App():
    return ft.SafeArea(
        content=ft.Router(
            [
                # Rota pública de Login (sem o menu/layout padrão)
                ft.Route(
                    path="login",
                    component=Login,
                ),
                # Rotas com a estrutura/menu principal (AppLayout)
                ft.Route(
                    component=AppLayout,
                    children=[
                        ft.Route(
                            path="inicio",
                            component=Home,
                        ),
                        ft.Route(
                            path="pdv",
                            component=lambda: ProtectedRoute("/pdv", PDV),
                        ),
                        # Produtos
                        ft.Route(
                            path="produtos",
                            component=lambda: ProtectedRoute("/produtos", Produtos),
                        ),
                        ft.Route(
                            path="produtos/novo",
                            component=NovoProduto,
                        ),
                        ft.Route(
                            path="produtos/editar/:id",
                            component=EditarProduto,
                        ),
                        # Pagamento e Caixa
                        ft.Route(
                            path="pagamento",
                            component=Pagamento,
                        ),
                        ft.Route(
                            path="caixa",
                            component=lambda: ProtectedRoute("/caixa", Caixa),
                        ),
                        ft.Route(
                            path="caixa/abrir",
                            component=AbrirCaixa,
                        ),
                        ft.Route(
                            path="caixa/suprimento",
                            component=lambda: MovimentacaoCaixa("SUPRIMENTO"),
                        ),
                        ft.Route(
                            path="caixa/sangria",
                            component=lambda: MovimentacaoCaixa("SANGRIA"),
                        ),
                        ft.Route(
                            path="caixa/fechar",
                            component=FecharCaixa,
                        ),
                        # Vendas
                        ft.Route(
                            path="vendas",
                            children=[
                                ft.Route(
                                    index=True,
                                    component=lambda: ProtectedRoute("/vendas", Vendas),
                                ),
                                ft.Route(
                                    path=":id",
                                    component=DetalhesVenda,
                                ),
                            ],
                        ),
                        # Dashboard e Configurações
                        ft.Route(
                            path="dashboard",
                            component=lambda: ProtectedRoute("/dashboard", Dashboard),
                        ),
                        ft.Route(
                            path="configuracoes",
                            component=lambda: ProtectedRoute(
                                "/configuracoes", Configuracoes
                            ),
                        ),
                    ],
                ),
            ]
        )
    )


if __name__ == "__main__":
    criar_tabelas()

    ft.run(lambda page: page.render(App), assets_dir="assets")
