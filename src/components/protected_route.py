from components import ft, AuthGuard



@ft.component
def ProtectedRoute(
        permission,
        component
):

    if not AuthGuard.verificar(permission):

        return ft.Container(

            expand=True,

            alignment=ft.Alignment.CENTER,

            content=ft.Column(

                [

                    ft.Icon(
                        ft.Icons.LOCK,
                        size=80,
                        color=ft.Colors.RED
                    ),

                    ft.Text(
                        "Acesso negado",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Text(
                        "Você não possui permissão para acessar esta página."
                    ),

                    ft.Button(

                        "Voltar",

                        on_click=lambda e:
                            ft.context.page.navigate("/inicio")
                    )

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        )

    return component()