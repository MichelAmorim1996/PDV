import json

from escpos.printer import Usb, Network


class ImpressoraService:

    def __init__(self, config_path="config.json"):

        with open(config_path, "r", encoding="utf-8") as arquivo:

            self.config = json.load(arquivo)

        self.loja = self.config["loja"]

        config_impressora = self.config["impressora"]

        tipo = config_impressora["tipo"].strip().upper()

        if tipo == "USB":

            self.printer = Usb(
                int(config_impressora["vendor_id"], 16),
                int(config_impressora["product_id"], 16),
                interface=int(config_impressora["interface"]),
                in_ep=int(config_impressora["in_ep"], 16),
                out_ep=int(config_impressora["out_ep"], 16),
            )

        elif tipo == "REDE":

            self.printer = Network(
                config_impressora["ip"], port=int(config_impressora["porta"])
            )

        else:

            raise ValueError(f"Tipo de impressora inválido: {tipo}")

    def imprimir_cupom(self, venda, itens):

        itens = self.normalizar_itens(itens)

        loja = self.loja

        self.printer.set(align="center", bold=True, width=2, height=2)

        self.printer.text(f"{loja['nome']}\n")

        self.printer.set(align="center", bold=False, width=1, height=1)

        self.printer.text(f"CNPJ: {loja['cnpj']}\n")

        self.printer.text(f"{loja['endereco']}\n")

        self.printer.text(f"Tel: {loja['telefone']}\n")

        self.printer.text("-" * 42 + "\n")

        self.printer.set(align="left")

        self.printer.text(f"VENDA: {venda['id']}\n")

        self.printer.text(f"DATA: {venda['data']}\n")

        self.printer.text("-" * 42 + "\n")

        for item in itens:

            descricao = item["descricao"]

            quantidade = item["quantidade"]

            preco = float(item["preco"])

            total = float(item["total"])

            self.printer.text(f"{descricao}\n")

            self.printer.text(
                f"{quantidade} x " f"R$ {preco:.2f}" f"       " f"R$ {total:.2f}\n"
            )

        self.printer.text("-" * 42 + "\n")

        self.printer.set(align="right", bold=True)

        self.printer.text(f"TOTAL: " f"R$ {float(venda['total']):.2f}\n")

        self.printer.set(align="left", bold=False)

        self.printer.text(f"Pagamento: " f"{venda['forma_pagamento']}\n")

        self.printer.text(
            "\nTenha Sempre uma experiencia \nsaborosa Com Sabor Festa!\n\n"
        )

        self.printer.cut()

    @staticmethod
    def normalizar_itens(itens):

        lista_normalizada = []

        for item in itens:

            lista_normalizada.append(
                {
                    "descricao": item["nome"],
                    "quantidade": item["quantidade"],
                    "preco": item["preco_unitario"],
                    "total": item["total"],
                }
            )

        return lista_normalizada

    def fechar(self):

        try:

            self.printer.close()

        except Exception as erro:

            print(f"Erro ao fechar impressora: {erro}")
