from views import ft, VendaController, ImpressoraController, carrinho, EstoqueInsuficienteError



@ft.component
def Pagamento():
    forma_pagamento, set_forma_pagamento = ft.use_state("Dinheiro")
    valor_recebido, set_valor_recebido = ft.use_state("")
    mensagem, set_mensagem = ft.use_state("")
    troco, set_troco = ft.use_state(0.0)

    total = carrinho.total()

    def finalizar():
        if not carrinho.itens:
            set_mensagem("O carrinho está vazio.")
            return

        if forma_pagamento == "Dinheiro":
            if not valor_recebido.strip():
                set_mensagem("Informe o valor recebido.")
                return
            try:
                recebido = float(valor_recebido.replace(",", ".").strip())
            except ValueError:
                set_mensagem("Informe um valor válido.")
                return
            if recebido < total:
                set_mensagem("O valor recebido é insuficiente.")
                return
            set_troco(recebido - total)
        else:
            set_troco(0.0)

        try:
            # Finalizar venda no banco
            id_venda = VendaController.finalizar_venda(carrinho.itens, forma_pagamento)

            # Buscar dados completos da venda
            dados_venda = VendaController.buscar_venda(id_venda)
            venda = dados_venda["venda"]
            itens = dados_venda["itens"]

            # Imprimir cupom
            ImpressoraController.imprimir_venda(venda, itens)

            # Limpar carrinho e voltar ao PDV
            carrinho.limpar()
            ft.context.page.navigate("/pdv")

        except EstoqueInsuficienteError as erro:
            set_mensagem(str(erro))
        except Exception as erro:
            set_mensagem(f"Erro ao finalizar venda: {erro}")

    def calcular_troco(e):
        valor = e.control.value
        set_valor_recebido(valor)

        try:
            recebido = float(valor.replace(",", "."))
            if recebido >= total:
                set_troco(recebido - total)
            else:
                set_troco(0.0)
        except ValueError:
            set_troco(0.0)

    return ft.Column(
        [
            ft.Text("Finalizar Venda", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Total da venda: R$ {total:.2f}", size=24),
            ft.Text("Forma de pagamento", size=18, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                value=forma_pagamento,
                options=[
                    ft.DropdownOption("Dinheiro"),
                    ft.DropdownOption("PIX"),
                    ft.DropdownOption("Cartão de débito"),
                    ft.DropdownOption("Cartão de crédito"),
                ],
                on_select=lambda e: set_forma_pagamento(e.control.value),
            ),
            ft.TextField(
                label="Valor recebido",
                value=valor_recebido,
                visible=(forma_pagamento == "Dinheiro"),
                on_change=calcular_troco,
            ),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Text(f"Troco: R$ {troco:.2f}", size=22, weight=ft.FontWeight.BOLD),
            ft.Row(
                [
                    ft.Button(
                        "Voltar",
                        on_click=lambda: ft.context.page.navigate("/pdv"),
                    ),
                    ft.Button(
                        "Confirmar venda",
                        icon=ft.Icons.CHECK,
                        on_click=finalizar,
                    ),
                ]
            ),
        ],
        spacing=20,
        width=600,
    )
