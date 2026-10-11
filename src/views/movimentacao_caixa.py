from views import ft, CaixaController


@ft.component
def MovimentacaoCaixa(tipo):

    valor, set_valor = ft.use_state("")

    descricao, set_descricao = ft.use_state("")

    mensagem, set_mensagem = ft.use_state("")

    titulo = "Suprimento" if tipo == "SUPRIMENTO" else "Sangria"

    def salvar():

        if not valor.strip():

            set_mensagem("Informe o valor.")

            return

        try:

            valor_numerico = float(valor.replace(",", ".").strip())

        except ValueError:

            set_mensagem("Informe um valor válido.")

            return

        try:

            if tipo == "SUPRIMENTO":

                CaixaController.suprimento(valor_numerico, descricao)

            else:

                CaixaController.sangria(valor_numerico, descricao)

            ft.context.page.navigate("/caixa")

        except ValueError as erro:

            set_mensagem(str(erro))

    return ft.Column(
        [
            ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label="Valor",
                value=valor,
                prefix="R$ ",
                on_change=lambda e: set_valor(e.control.value),
            ),
            ft.TextField(
                label="Descrição",
                value=descricao,
                multiline=True,
                on_change=lambda e: set_descricao(e.control.value),
            ),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Row(
                [
                    ft.Button(
                        "Cancelar", on_click=lambda: ft.context.page.navigate("/caixa")
                    ),
                    ft.Button("Confirmar", on_click=salvar),
                ]
            ),
        ],
        spacing=20,
        width=500,
    )
