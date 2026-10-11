from services import sessao, PermissionService

class AuthGuard:

    @staticmethod
    def verificar(rota):

        if not sessao.logado:
            return False

        return PermissionService.pode_acessar(
            sessao.usuario,
            rota
        )