import flet as ft
from database.database import criar_tabelas
from views.layout import AppLayout
from views.home import Home
from views.pdv import PDV
from views.produtos import Produtos
from views.novo_produto import NovoProduto
from views.editar_produto import EditarProduto
from views.pagamento import Pagamento
from views.caixa import Caixa
from views.abrir_caixa import AbrirCaixa
from views.movimentacao_caixa import MovimentacaoCaixa
from views.fechar_caixa import FecharCaixa
from views.vendas import Vendas
from views.detalhes_venda import DetalhesVenda
from views.dashboard import Dashboard
from views.configuracoes import Configuracoes
from views.login import Login
from components.protected_route import ProtectedRoute

__all__ = [
    "ft",
    "criar_tabelas",
    "AppLayout",
    "Home",
    "PDV",
    "Produtos",
    "NovoProduto",
    "EditarProduto",
    "Pagamento",
    "Caixa",
    "AbrirCaixa",
    "MovimentacaoCaixa",
    "FecharCaixa",
    "Vendas",
    "DetalhesVenda",
    "Dashboard",
    "Configuracoes",
    "Login",
    "ProtectedRoute",
]
