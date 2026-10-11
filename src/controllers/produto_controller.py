from controllers import ProdutoModel

class ProdutoController:

    @staticmethod
    def listar():
        return ProdutoModel.listar()

    @staticmethod
    def buscar(nome):
        if not nome:
            return ProdutoModel.listar()
        return ProdutoModel.buscar_por_nome(nome)

    @staticmethod
    def buscar_por_id(produto_id):
        return ProdutoModel.buscar_por_id(produto_id)

    @staticmethod
    def cadastrar(codigo, nome, categoria,
                  preco_custo, preco_venda,
                  estoque, estoque_minimo):
        return ProdutoModel.cadastrar(
            codigo,
            nome,
            categoria,
            preco_custo,
            preco_venda,
            estoque,
            estoque_minimo
        )

    @staticmethod
    def atualizar(produto_id, codigo, nome, categoria,
                  preco_custo, preco_venda, estoque, estoque_minimo):
        return ProdutoModel.atualizar(
            produto_id,
            codigo,
            nome,
            categoria,
            preco_custo,
            preco_venda,
            estoque,
            estoque_minimo
        )

    @staticmethod
    def excluir(produto_id):
        return ProdutoModel.excluir(produto_id)
