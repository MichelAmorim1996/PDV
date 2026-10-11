from views import *
from controllers.caixa_controller import CaixaController

@ft.component
def AbrirCaixa():
    valor_inicial, set_valor_inicial = ft.use_state("")

    mensagem, set_mensagem = ft.use_state("")

    def abrir():

        if not valor_inicial.strip():

            set_mensagem("Informe o valor inicial.")

            return

        try:

            valor = float(valor_inicial.replace(",", ".").strip())

        except ValueError:

            set_mensagem("Informe um valor válido.")

            return

        try:

            CaixaController.abrir(valor)

            ft.context.page.navigate("/caixa")

        except ValueError as erro:

            set_mensagem(str(erro))

    return ft.Column(
        [
            ft.Text("Abrir Caixa", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Informe o valor inicial " "disponível no caixa."),
            ft.TextField(
                label="Valor inicial",
                value=valor_inicial,
                prefix="R$ ",
                on_change=lambda e: set_valor_inicial(e.control.value),
            ),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Button("Abrir caixa", icon=ft.Icons.LOCK_OPEN, on_click=abrir),
        ],
        spacing=20,
        width=500,
    )
