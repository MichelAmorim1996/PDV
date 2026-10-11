from controllers import UsuarioModel

class ConfiguracaoController:


    @staticmethod
    def salvar(nome, cnpj, endereco, telefone,
               tipo_impressora, ip, porta,
               vendor_id=None, product_id=None,
               interface=None, in_ep=None, out_ep=None):
        configuracoes = {
            "loja": {
                "nome": nome,
                "cnpj": cnpj,
                "endereco": endereco,
                "telefone": telefone,
            },
            "impressora": {
                "tipo": tipo_impressora,
                "ip": ip,
                "porta": porta,
                "vendor_id": vendor_id,
                "product_id": product_id,
                "interface": interface,
                "in_ep": in_ep,
                "out_ep": out_ep,
            },
        }
        import json
        with open("config.json", "w") as f:
            json.dump(configuracoes, f, indent=4)

    @staticmethod
    def carregar():
        import json
        with open("config.json", "r") as f:
            return json.load(f)

    ...

    @staticmethod
    def alterar_senha_vendedor(usuario, senha):

        UsuarioModel.alterar_senha(
            usuario,
            senha
        )