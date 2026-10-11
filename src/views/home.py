from views import ft, ConfiguracaoController, BotaoAcao, sessao, PermissionService, MENU

@ft.component
def Home():
    dados = ConfiguracaoController.carregar()
    dados = dados["loja"]

    usuario = sessao.usuario
    nivel = usuario["nivel"]

    permissoes = PermissionService.permissoes[nivel.upper()]
    acoes = []

    for permissao in permissoes:
        chave = permissao.lstrip("/")  # remove a barra inicial
        if chave in MENU:
            item = MENU[chave]
            acoes.append(BotaoAcao(item["nome"], item["icone"], item["rota"]))
    page = ft.context.page

    def logout(rota):
        page.navigate(rota)
        sessao.logado = False

    return ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Image(src="logo.png", width=120),
                                        ft.Text(
                                            dados["nome"],
                                            color=ft.Colors.RED_500,
                                            size=32,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ]
                                ),
                                ft.Text(
                                    "Powered by: BPG STORE SOLUÇÕES: Gerencie sua loja de forma simples e rápida",
                                    size=16,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_size=28,
                            on_click=lambda e: logout("/login"),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=30),
                # CARDS DE RESUMO
                ft.Container(height=25),
                # AÇÕES RÁPIDAS
                ft.Text("Ações rápidas", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    acoes,
                    spacing=20,
                    wrap=True,
                ),
                ft.Container(height=25),
            ],
            expand=True,
            height=ft.context.page.height,
            scroll=ft.ScrollMode.AUTO,
        ),
    )


@ft.component
def CardResumo(titulo, valor, icone, rota):

    return ft.Card(
        expand=True,
        content=ft.Container(
            padding=20,
            on_click=lambda e: ft.context.page.navigate(rota),
            content=ft.Row(
                [
                    ft.Icon(icone, size=40),
                    ft.Column(
                        [
                            ft.Text(titulo, size=15),
                            ft.Text(valor, size=25, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=5,
                    ),
                ]
            ),
        ),
    )
