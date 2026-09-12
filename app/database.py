"""
Liga à base de dados SQLite e guarda o histórico de execuções das automações.
"""
import sqlite3
from datetime import datetime
from pathlib import Path

CAMINHO_BD = Path(__file__).parent.parent / "portal.db"


def obter_ligacao():
    ligacao = sqlite3.connect(CAMINHO_BD)
    ligacao.row_factory = sqlite3.Row
    return ligacao


def inicializar_bd():
    ligacao = obter_ligacao()
    ligacao.execute(
        """
        CREATE TABLE IF NOT EXISTS execucoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa TEXT NOT NULL,
            sucesso INTEGER NOT NULL,
            mensagem TEXT,
            duracao_segundos REAL,
            executado_em TEXT NOT NULL
        )
        """
    )
    ligacao.commit()
    ligacao.close()


def registar_execucao(tarefa: str, sucesso: bool, mensagem: str, duracao_segundos: float):
    ligacao = obter_ligacao()
    ligacao.execute(
        "INSERT INTO execucoes (tarefa, sucesso, mensagem, duracao_segundos, executado_em) "
        "VALUES (?, ?, ?, ?, ?)",
        (tarefa, int(sucesso), mensagem, duracao_segundos, datetime.now().isoformat(timespec="seconds")),
    )
    ligacao.commit()
    ligacao.close()


def obter_historico(limite: int = 50):
    ligacao = obter_ligacao()
    linhas = ligacao.execute(
        "SELECT * FROM execucoes ORDER BY id DESC LIMIT ?", (limite,)
    ).fetchall()
    ligacao.close()
    return linhas