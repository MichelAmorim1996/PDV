class CarrinhoState:

    def __init__(self):

        self.itens = []

    def adicionar(self, produto, quantidade=1):

        for item in self.itens:

            if item["id"] == produto["id"]:

                item["quantidade"] += quantidade

                item["total"] = item["quantidade"] * item["preco_unitario"]

                return

        self.itens.append(
            {
                "id": produto["id"],
                "nome": produto["nome"],
                "preco_unitario": produto["preco_venda"],
                "quantidade": quantidade,
                "total": produto["preco_venda"] * quantidade,
            }
        )

    def remover(self, produto_id):

        self.itens = [item for item in self.itens if item["id"] != produto_id]

    def aumentar(self, produto_id):

        for item in self.itens:

            if item["id"] == produto_id:

                item["quantidade"] += 1

                item["total"] = item["quantidade"] * item["preco_unitario"]

    def diminuir(self, produto_id):

        for item in self.itens:

            if item["id"] == produto_id:

                item["quantidade"] -= 1

                if item["quantidade"] <= 0:

                    self.remover(produto_id)

                else:

                    item["total"] = item["quantidade"] * item["preco_unitario"]

    def total(self):

        return sum(item["total"] for item in self.itens)

    def limpar(self):

        self.itens.clear()
