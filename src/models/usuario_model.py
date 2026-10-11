from models import conectar


class UsuarioModel:
    def __init__(self, row):
        self.id = row["id"]
        self.nome = row["nome"]
        self.usuario = row["usuario"]
        self.nivel = row["nivel"]

    @staticmethod
    def login(usuario, senha):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha)
        )
        row = cursor.fetchone()
        return UsuarioModel(row) if row else None

    @staticmethod
    def alterar_senha(usuario, senha):

        conexao = conectar()

        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE usuarios
            SET senha = ?
            WHERE usuario = ?
            """,
            (senha, usuario),
        )

        conexao.commit()

        conexao.close()
