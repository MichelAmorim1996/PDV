from views import ft, CaixaController



@ft.component
def FecharCaixa():

    valor_contado, set_valor_contado = ft.use_state("")

    mensagem, set_mensagem = ft.use_state("")

    resultado, set_resultado = ft.use_state(None)

    def fechar():

        try:

            valor = float(valor_contado.replace(",", "."))

            id_caixa = CaixaController.caixa_aberto()["id"]

            resultado_fechamento = CaixaController.fechar_caixa(id_caixa, valor)

            set_resultado(resultado_fechamento)

        except ValueError as erro:

            set_mensagem(str(erro))

    return ft.Column(
        [
            ft.Text("Fechamento de Caixa", size=28, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label="Valor contado",
                prefix="R$ ",
                value=valor_contado,
                on_change=lambda e: set_valor_contado(e.control.value),
            ),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Button("Fechar caixa", icon=ft.Icons.LOCK, on_click=fechar),
            (
                ft.Column(
                    [
                        ft.Text("Caixa fechado com sucesso!", size=22),
                        ft.Text(
                            f"Esperado: " f"R$ " f"{resultado['valor_esperado']:.2f}"
                        ),
                        ft.Text(
                            f"Contado: " f"R$ " f"{resultado['valor_contado']:.2f}"
                        ),
                        ft.Text(f"Diferença: " f"R$ " f"{resultado['diferenca']:.2f}"),
                    ]
                )
                if resultado
                else ft.Container()
            ),
        ],
        spacing=20,
        width=600,
    )
