from services import sessao

class PermissionService:

    permissoes = {

        "ADMIN": [
            "/inicio",
            "/pdv",
            "/produtos",
            "/vendas",
            "/caixa",
            "/dashboard",
            "/configuracoes",
        ],

        "VENDEDOR": [
            "/inicio",
            "/pdv",
            "/vendas",
        ],

        "CAIXA": [
            "/inicio",
            "/produtos"
            "/caixa",
            "/vendas",
        ]
    }

    @classmethod
    def pode_acessar(cls, usuario, rota):

        if usuario is None:
            return False

        nivel = usuario["nivel"].upper()

        return rota in cls.permissoes.get(nivel, [])