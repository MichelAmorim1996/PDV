from views import ft, AuthController,ConfiguracaoController, sessao




@ft.component
def Login():
    dados = ConfiguracaoController.carregar()
    dados = dados["loja"]

    usuario, set_usuario = ft.use_state("")
    senha, set_senha = ft.use_state("")
    erro, set_erro = ft.use_state("")

    def entrar():

        dados = AuthController.login(usuario, senha)

        if dados:
            ft.context.page.navigate("/inicio")
        else:
            set_erro("Usuário ou senha inválidos")

    return ft.Container(
        alignment=ft.Alignment.CENTER,
        expand=True,
        content=ft.Card(
            content=ft.Container(
                width=420,
                padding=40,
                content=ft.Row(ft.Column(
                    [
                        ft.Image(src="logo.png", width=150),
                        ft.Text(dados["nome"], size=28, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(
                            label="Usuário",
                            value=usuario,
                            options=[
                                ft.DropdownOption("admin"),
                                ft.DropdownOption("vendedor"),
                            ],
                            width=270,
                            on_select=lambda e: set_usuario(e.control.value),
                        ),
                        ft.TextField(
                            label="Senha",
                            value=senha,
                            width=270,
                            password=True,
                            can_reveal_password=True,
                            on_change=lambda e: set_senha(e.control.value),
                            on_submit=lambda e: entrar()
                        ),
                        ft.Text(erro, color=ft.Colors.RED),
                        ft.Button("Entrar", width=300, on_click=lambda e: entrar()),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
   
                ),vertical_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ),
    )
