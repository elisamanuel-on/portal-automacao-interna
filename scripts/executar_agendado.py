"""
Script para ser chamado pelo cron do Ubuntu.

Corre uma das automações do portal (aqui, o backup) e regista o
resultado no histórico do portal, exatamente como se tivesse sido
clicado o botão "Executar" na página.

Uso:
    python scripts/executar_agendado.py
"""
import sys
import time
from pathlib import Path

# Garante que o pacote "app" é encontrado, independentemente de onde
# o script for chamado (importante para o cron, que não corre a
# partir desta pasta por omissão).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import automacoes, database

if __name__ == "__main__":
    database.inicializar_bd()

    inicio = time.perf_counter()
    sucesso, mensagem = automacoes.fazer_backup()
    duracao = time.perf_counter() - inicio

    database.registar_execucao("Fazer Backup (agendado)", sucesso, mensagem, duracao)

    estado = "OK" if sucesso else "FALHOU"
    print(f"[{estado}] {mensagem}")