from views import ft, VendaController, ImpressoraController

@ft.component
def DetalhesVenda():
    params = ft.use_route_params()

    try:
        id_venda = int(params.get("id", 0))
    except (ValueError, TypeError):
        return ft.Text("ID da venda inválido.", size=24)

    dados = VendaController.buscar_venda(id_venda)
    mensagem, set_mensagem = ft.use_state("")

    if not dados:
        return ft.Column(
            [
                ft.Text("Venda não encontrada.", size=24),
                ft.Button(
                    "Voltar",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda: ft.context.page.navigate("/vendas"),
                ),
            ],
            spacing=20,
        )

    venda = dados["venda"]
    itens = dados["itens"]

    produtos = [
        ft.Card(
            content=ft.ListTile(
                title=ft.Text(item["nome"]),
                subtitle=ft.Text(
                    f"{item['quantidade']} x R$ {item['preco_unitario']:.2f}"
                ),
                trailing=ft.Text(
                    f"R$ {item['total']:.2f}",
                    weight=ft.FontWeight.BOLD,
                ),
            )
        )
        for item in itens
    ]

    # Funções de diálogo
    def fechar_dialog(e=None):
        ft.context.page.pop_dialog()

    def confirmar_cancelamento(e=None):
        try:
            VendaController.cancelar_venda(id_venda)
            set_mensagem("Venda cancelada com sucesso.")
            ft.context.page.navigate("/vendas")
        except Exception as erro:
            set_mensagem(str(erro))
        finally:
            fechar_dialog()

    def abrir_dialog_cancelamento(e=None):

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cancelar venda?"),
            content=ft.Text(
                "Esta ação irá cancelar a venda, "
                "devolver os produtos ao estoque e "
                "registrar o estorno no caixa."
            ),
            actions=[
                ft.TextButton(content="Não", on_click=fechar_dialog),
                ft.Button(
                    content="Sim, cancelar",
                    icon=ft.Icons.CANCEL,
                    on_click=confirmar_cancelamento,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        ft.context.page.show_dialog(dialog)

    # Função de impressão
    def imprimir_cupom(e=None):
        try:
            ImpressoraController.imprimir_venda(venda, itens)
            set_mensagem("Cupom impresso com sucesso.")
        except Exception as erro:
            set_mensagem(f"Erro ao imprimir cupom: {erro}")

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Button(
                        "Voltar",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda: ft.context.page.navigate("/vendas"),
                    ),
                    ft.Text(
                        f"Venda #{venda['id']}", size=28, weight=ft.FontWeight.BOLD
                    ),
                ]
            ),
            ft.Divider(),
            ft.Text(f"Data: {venda['data']}"),
            ft.Text(f"Status: {venda['status']}"),
            ft.Text(f"Pagamento: {venda['forma_pagamento']}"),
            ft.Divider(),
            ft.Text("Produtos", size=22, weight=ft.FontWeight.BOLD),
            ft.Column(produtos, scroll=ft.ScrollMode.AUTO, expand=True),
            ft.Divider(),
            ft.Text(
                f"Total: R$ {venda['total']:.2f}", size=24, weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                mensagem,
                color=ft.Colors.RED if "erro" in mensagem.lower() else ft.Colors.GREEN,
            ),
            ft.Row(
                [
                    ft.Button(
                        "Cancelar venda",
                        icon=ft.Icons.CANCEL,
                        on_click=abrir_dialog_cancelamento,
                        disabled=(venda["status"] == "CANCELADA"),
                    ),
                    ft.Button(
                        "Imprimir cupom",
                        icon=ft.Icons.PRINT,
                        on_click=imprimir_cupom,
                        disabled=(venda["status"] != "FINALIZADA"),
                    ),
                ]
            ),
        ],
        spacing=15,
        expand=True,
        height=ft.context.page.height - 100,
        scroll=ft.ScrollMode.AUTO,
    )
