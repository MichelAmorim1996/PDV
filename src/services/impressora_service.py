import json
import sys

from pathlib import Path

import usb.backend.libusb1

from escpos.printer import Usb, Network

from services.caminho_service import obter_caminho_config





def localizar_libusb():

    if getattr(sys, "frozen", False):

        base = Path(sys.executable).parent

    else:

        base = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            .parent
        )

    dll = base / "libusb-1.0.dll"

    if not dll.exists():

        raise FileNotFoundError(
            f"libusb-1.0.dll não encontrada em: {dll}"
        )

    return dll


def obter_backend_usb():

    caminho_dll = localizar_libusb()

    backend = usb.backend.libusb1.get_backend(
        find_library=lambda _: caminho_dll
    )

    if backend is None:

        raise RuntimeError(
            f"Não foi possível carregar o backend libusb:\n"
            f"{caminho_dll}"
        )

    return backend


class ImpressoraService:

    def __init__(self, config_path=None):

        if config_path is None:

            config_path = obter_caminho_config()

        with open(

            config_path,

            "r",

            encoding="utf-8"

        ) as arquivo:

            self.config = json.load(arquivo)

        self.loja = self.config["loja"]

        config_impressora = self.config["impressora"]

        tipo = (

            config_impressora["tipo"]

            .strip()

            .upper()

        )

        if tipo == "USB":

            backend = obter_backend_usb()

            self.printer = Usb(

                int(

                    config_impressora["vendor_id"],

                    16

                ),

                int(

                    config_impressora["product_id"],

                    16

                ),

                interface=int(

                    config_impressora["interface"]

                ),

                in_ep=int(

                    config_impressora["in_ep"],

                    16

                ),

                out_ep=int(

                    config_impressora["out_ep"],

                    16

                ),

                backend=backend

            )

        elif tipo == "REDE":

            self.printer = Network(

                config_impressora["ip"],

                port=int(

                    config_impressora["porta"]

                )

            )

        else:

            raise ValueError(

                f"Tipo de impressora inválido: {tipo}"

            )

    def imprimir_cupom(self, venda, itens):

        itens = self.normalizar_itens(itens)

        loja = self.loja

        self.printer.set(

            align="center",

            bold=True,

            width=2,

            height=2

        )

        self.printer.text(

            f"{loja['nome']}\n"

        )

        self.printer.set(

            align="center",

            bold=False,

            width=1,

            height=1

        )

        self.printer.text(

            f"CNPJ: {loja['cnpj']}\n"

        )

        self.printer.text(

            f"{loja['endereco']}\n"

        )

        self.printer.text(

            f"Tel: {loja['telefone']}\n"

        )

        self.printer.text(

            "-" * 42 + "\n"

        )

        self.printer.set(

            align="left"

        )

        self.printer.text(

            f"VENDA: {venda['id']}\n"

        )

        self.printer.text(

            f"DATA: {venda['data']}\n"

        )

        self.printer.text(

            "-" * 42 + "\n"

        )

        for item in itens:

            descricao = item["descricao"]

            quantidade = item["quantidade"]

            preco = float(item["preco"])

            total = float(item["total"])

            self.printer.text(

                f"{descricao}\n"

            )

            self.printer.text(

                f"{quantidade} x "

                f"R$ {preco:.2f}"

                f"       "

                f"R$ {total:.2f}\n"

            )

        self.printer.text(

            "-" * 42 + "\n"

        )

        self.printer.set(

            align="right",

            bold=True

        )

        self.printer.text(

            f"TOTAL: "

            f"R$ {float(venda['total']):.2f}\n"

        )

        self.printer.set(

            align="left",

            bold=False

        )

        self.printer.text(

            f"Pagamento: "

            f"{venda['forma_pagamento']}\n"

        )

        self.printer.text(

            "\nTenha sempre uma experiência\n"

            "saborosa com Sabor Festa!\n\n"

        )

        self.printer.cut()

    @staticmethod

    def normalizar_itens(itens):

        lista_normalizada = []

        for item in itens:

            lista_normalizada.append({

                "descricao": item["nome"],

                "quantidade": item["quantidade"],

                "preco": item["preco_unitario"],

                "total": item["total"]

            })

        return lista_normalizada

    def fechar(self):

        try:

            self.printer.close()

        except Exception as erro:

            print(

                f"Erro ao fechar impressora: {erro}"

            )