from views import ft, ConfiguracaoController

@ft.component
def Configuracoes():

    configuracoes = ConfiguracaoController.carregar()
    loja = configuracoes["loja"]
    impressora = configuracoes["impressora"]

    # Estado para nova senha
    usuario, set_usuario = ft.use_state("vendendor")
    nova_senha, set_nova_senha = ft.use_state("")
    confirmar_senha, set_confirmar_senha = ft.use_state("")

    # Estados da loja
    nome, set_nome = ft.use_state(loja["nome"])
    cnpj, set_cnpj = ft.use_state(loja["cnpj"])
    endereco, set_endereco = ft.use_state(loja["endereco"])
    telefone, set_telefone = ft.use_state(loja["telefone"])

    # Estados da impressora
    tipo_impressora, set_tipo_impressora = ft.use_state(impressora["tipo"])
    ip, set_ip = ft.use_state(impressora["ip"])
    porta, set_porta = ft.use_state(str(impressora["porta"]))

    # Estados USB
    vendor_id, set_vendor_id = ft.use_state(str(impressora.get("vendor_id", "")))
    product_id, set_product_id = ft.use_state(str(impressora.get("product_id", "")))
    interface, set_interface = ft.use_state(str(impressora.get("interface", "0")))
    in_ep, set_in_ep = ft.use_state(str(impressora.get("in_ep", "0x81")))
    out_ep, set_out_ep = ft.use_state(str(impressora.get("out_ep", "0x03")))

    mensagem, set_mensagem = ft.use_state("")
    sucesso, set_sucesso = ft.use_state("")

    def salvar():
        try:
            ConfiguracaoController.salvar(
                nome,
                cnpj,
                endereco,
                telefone,
                tipo_impressora,
                ip,
                porta,
                vendor_id,
                product_id,
                interface,
                in_ep,
                out_ep
            )
            set_sucesso("Configurações salvas com sucesso.")
            set_mensagem("")
        except Exception as erro:
            set_mensagem(str(erro))

    def alterar_senha():

        if nova_senha.strip() == "":
            set_mensagem("Informe uma nova senha.")
            return

        if nova_senha != confirmar_senha:
            set_mensagem("As senhas não conferem.")
            return

        try:
            ConfiguracaoController.alterar_senha_vendedor(
                usuario,
                nova_senha
            )

            set_sucesso("Senha alterada com sucesso.")

            set_mensagem("")

            set_nova_senha("")
            set_confirmar_senha("")

        except Exception as erro:

            set_mensagem(str(erro))

    

    return ft.Column(
        [
            ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD),
            #ft.Divider(),
            #ft.Text("Dados da loja", size=22, weight=ft.FontWeight.BOLD),
            #ft.TextField(label="Nome da loja", value=nome, on_change=lambda e: set_nome(e.control.value)),
            #ft.TextField(label="CNPJ", value=cnpj, on_change=lambda e: set_cnpj(e.control.value)),
            #ft.TextField(label="Endereço", value=endereco, on_change=lambda e: set_endereco(e.control.value)),
            #ft.TextField(label="Telefone", value=telefone, on_change=lambda e: set_telefone(e.control.value)),
            ft.Divider(),
            ft.Text("Impressora", size=22, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                label="Tipo de conexão",
                value=tipo_impressora,
                options=[ft.DropdownOption("REDE"), ft.DropdownOption("USB")],
                on_select=lambda e: set_tipo_impressora(e.control.value)
            ),
            # Campos REDE
            ft.TextField(label="IP da impressora", value=ip, visible=(tipo_impressora == "REDE"),
                         on_change=lambda e: set_ip(e.control.value)),
            ft.TextField(label="Porta", value=porta, visible=(tipo_impressora == "REDE"),
                         on_change=lambda e: set_porta(e.control.value)),
            # Campos USB
            ft.TextField(
                label="Vendor ID", 
                value=vendor_id, 
                visible=(tipo_impressora == "USB"),
                on_change=lambda e: set_vendor_id(e.control.value)),
            ft.TextField(label="Product ID", value=product_id, visible=(tipo_impressora == "USB"),
                         on_change=lambda e: set_product_id(e.control.value)),
            ft.TextField(label="Interface", value=interface, visible=(tipo_impressora == "USB"),
                         on_change=lambda e: set_interface(e.control.value)),
            ft.TextField(label="Endpoint IN", value=in_ep, visible=(tipo_impressora == "USB"),
                         on_change=lambda e: set_in_ep(e.control.value)),
            ft.TextField(label="Endpoint OUT", value=out_ep, visible=(tipo_impressora == "USB"),
                         on_change=lambda e: set_out_ep(e.control.value)),
            ft.Text(mensagem, color=ft.Colors.RED),
            ft.Text(sucesso, color=ft.Colors.GREEN),
            ft.Button("Salvar configurações", icon=ft.Icons.SAVE, on_click=salvar),


            ft.Divider(),

            ft.Text(
                "Gerenciar Login",
                size=22,
                weight=ft.FontWeight.BOLD
            ),

            ft.Dropdown(
                label="Usuario",
                value=usuario,
                options=[
                    ft.DropdownOption("admin"),
                    ft.DropdownOption("vendedor"),
                ],
                on_select=lambda e: set_usuario(e.control.value),
            ),

            ft.TextField(
                label="Nova senha",
                password=True,
                can_reveal_password=True,
                value=nova_senha,
                on_change=lambda e:
                    set_nova_senha(e.control.value)
            ),

            ft.TextField(
                label="Confirmar senha",
                password=True,
                can_reveal_password=True,
                value=confirmar_senha,
                on_change=lambda e:
                    set_confirmar_senha(e.control.value)
            ),

            ft.Button(
                "Alterar senha",
                icon=ft.Icons.LOCK_RESET,
                on_click=lambda e:
                    alterar_senha()
            ),




        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        height=ft.context.page.height-100
    )
