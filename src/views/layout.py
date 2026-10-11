from views import ft, NavLink, sessao, NavLink, PermissionService
from services.permission_service import PermissionService


@ft.component
def AppLayout():

    if sessao.usuario is None:
        ft.context.page.navigate("/login")

        return  # evita continuar sem usuário

    rotas = PermissionService.permissoes[sessao.usuario["nivel"]]

    ft.context.page.title = "Sabor Festa powered by BPGSTORE"
    ft.context.page.theme_mode = ft.ThemeMode.LIGHT
    ft.context.page.window.full_screen = True
    outlet = ft.use_route_outlet()

    # Gerar links dinamicamente
    links = []

    icones = {
        "/inicio": ft.Icons.HOME,
        "/pdv": ft.Icons.POINT_OF_SALE,
        "/produtos": ft.Icons.INVENTORY,
        "/vendas": ft.Icons.RECEIPT,
        "/caixa": ft.Icons.ACCOUNT_BALANCE_WALLET,
        "/dashboard": ft.Icons.BAR_CHART,
        "/configuracoes": ft.Icons.SETTINGS,
    }
    for rota in rotas:

        links.append(
            NavLink(
                rota.replace("/", "").capitalize() if rota != "/inicio" else "Início",
                rota,
                # icones[rota]
            )
        )

    return ft.Column(
        [
            ft.Row(links, spacing=10),
            ft.Divider(),
            outlet,
        ],
        expand=True,
        width=ft.context.page.width,
    )
