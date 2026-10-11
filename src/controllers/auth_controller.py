from controllers import UsuarioModel, sessao


class AuthController:

    @staticmethod
    def login(usuario, senha):
        user = UsuarioModel.login(usuario, senha)
        if user:
            sessao.usuario = {
                "id": user.id,
                "nome": user.nome,
                "nivel": user.nivel
            }
            sessao.logado = True
        return user
