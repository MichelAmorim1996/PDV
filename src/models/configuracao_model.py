from models import json, Path



class ConfiguracaoModel:

    ARQUIVO = Path("configuracoes.json")

    @classmethod
    def carregar(cls):

        if not cls.ARQUIVO.exists():

            configuracoes = {
                "loja": {
                    "nome": "Minha Loja",
                    "cnpj": "",
                    "endereco": "",
                    "telefone": "",
                },
                "impressora": {"tipo": "REDE", "ip": "", "porta": 9100},
            }

            cls.salvar(configuracoes)

            return configuracoes

        with open(cls.ARQUIVO, "r", encoding="utf-8") as arquivo:

            return json.load(arquivo)

    @classmethod
    def salvar(cls, configuracoes):

        with open(cls.ARQUIVO, "w", encoding="utf-8") as arquivo:

            json.dump(configuracoes, arquivo, indent=4, ensure_ascii=False)
