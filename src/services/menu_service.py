from services import ft

MENU = {

    "pdv": {
        "nome": "Nova venda",
        "icone": ft.Icons.POINT_OF_SALE,
        "rota": "/pdv"
    },

    "produtos": {
        "nome": "Produtos",
        "icone": ft.Icons.INVENTORY_2,
        "rota": "/produtos"
    },

    "vendas": {
        "nome": "Vendas",
        "icone": ft.Icons.RECEIPT_LONG,
        "rota": "/vendas"
    },

    "caixa": {
        "nome": "Caixa",
        "icone": ft.Icons.ACCOUNT_BALANCE_WALLET,
        "rota": "/caixa"
    }

}