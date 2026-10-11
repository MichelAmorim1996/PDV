from views import ft, EstoqueController



@ft.component
def EntradaEstoque():

    id_produto, set_id_produto = ft.use_state("")

    quantidade, set_quantidade = ft.use_state("")

    motivo, set_motivo = ft.use_state("")

    mensagem, set_mensagem = ft.use_state("")

    def salvar():

        try:

            EstoqueController.entrada(
                int(id_produto), float(quantidade.replace(",", ".")), motivo
            )

            ft.context.page.navigate("/estoque")

        except Exception as erro:

            set_mensagem(str(erro))

    return ft.Column(
        [
            ft.Text("Entrada de Estoque", size=28, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label="ID do produto",
                on_change=lambda e: set_id_produto(e.control.value),
            ),
            ft.TextField(
                label="Quantidade", on_change=lambda e: set_quantidade(e.control.value)
            ),
            ft.TextField(
                label="Motivo", on_change=lambda e: set_motivo(e.control.value)
            ),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Button("Confirmar entrada", on_click=salvar),
        ],
        spacing=20,
        width=500,
    )
