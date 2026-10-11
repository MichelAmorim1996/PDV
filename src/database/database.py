import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "pdv.db"


# DATABASE = "dados.db"


def conectar():

    conexao = sqlite3.connect(DATABASE)

    conexao.row_factory = sqlite3.Row

    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao


def criar_tabelas():

    with conectar() as conexao:

        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caixas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_abertura TEXT NOT NULL,
                data_fechamento TEXT,
                valor_inicial REAL NOT NULL,
                valor_final REAL,
                valor_esperado REAL,   -- nova coluna
                diferenca REAL,        -- nova coluna
                status TEXT NOT NULL
            )

        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes_caixa (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                id_caixa INTEGER NOT NULL,

                tipo TEXT NOT NULL,

                valor REAL NOT NULL,

                descricao TEXT,

                data TEXT NOT NULL,

                FOREIGN KEY (
                    id_caixa
                )

                REFERENCES caixas(id)

            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                codigo TEXT UNIQUE NOT NULL,

                nome TEXT NOT NULL,

                categoria TEXT NOT NULL,

                preco_custo REAL DEFAULT 0,

                preco_venda REAL NOT NULL,

                estoque REAL DEFAULT 0,

                estoque_minimo REAL DEFAULT 0,

                ativo INTEGER DEFAULT 1,

                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP

            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                id_caixa INTEGER NOT NULL,

                data TEXT NOT NULL,

                subtotal REAL NOT NULL,

                desconto REAL DEFAULT 0,

                acrescimo REAL DEFAULT 0,

                total REAL NOT NULL,

                status TEXT NOT NULL,

                FOREIGN KEY (
                    id_caixa
                )

                REFERENCES caixas(id)

            )
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade REAL NOT NULL,
            preco_unitario REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (id_venda) REFERENCES vendas(id),
            FOREIGN KEY (id_produto) REFERENCES produtos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            forma_pagamento TEXT NOT NULL,
            valor REAL NOT NULL,
            FOREIGN KEY (id_venda) REFERENCES vendas(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_produto INTEGER NOT NULL,

            tipo TEXT NOT NULL,

            quantidade REAL NOT NULL,

            estoque_anterior REAL NOT NULL,

            estoque_posterior REAL NOT NULL,

            motivo TEXT,

            data TEXT NOT NULL,

            FOREIGN KEY (

                id_produto

            )

            REFERENCES produtos(id)

        )

    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel TEXT NOT NULL,
            ativo INTEGER DEFAULT 1,
            primeiro_acesso INTEGER DEFAULT 1,
            ultimo_login TEXT,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
        
        )
        """)

    cursor.execute("""
        SELECT COUNT(*) FROM usuarios
        """)
    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO usuarios
            (
                nome,
                usuario,
                senha,
                nivel
            )
            VALUES
            (
                'Administrador',
                'admin',
                '451234',
                'ADMIN'
            )
            """)
        cursor.execute("""
                INSERT INTO usuarios
                (
                    nome,
                    usuario,
                    senha,
                    nivel
                )
                VALUES
                (
                    'Vendedor',
                    'vendedor',
                    '1234',
                    'VENDEDOR'
                )
                """)
    conexao.commit()
