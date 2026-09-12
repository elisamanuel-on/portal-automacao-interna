"""
Portal de Automação Interna — dispara automações e mostra o histórico.

Corre com: uvicorn app.main:app --reload
"""
import time

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import automacoes, database

app = FastAPI(title="Portal de Automação Interna")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

database.inicializar_bd()

TAREFAS = {
    "organizar-ficheiros": ("Organizar Ficheiros", automacoes.organizar_ficheiros),
    "gerar-relatorio": ("Gerar Relatório", automacoes.gerar_relatorio),
    "fazer-backup": ("Fazer Backup", automacoes.fazer_backup),
}

# Só os nomes (texto) vão para o template — o Jinja2 não lida bem com
# dicionários cujos valores incluem funções, por isso as funções ficam
# só do lado do Python.
NOMES_TAREFAS = {chave: nome for chave, (nome, _) in TAREFAS.items()}


@app.get("/")
def pagina_inicial(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"tarefas": NOMES_TAREFAS}
    )


@app.post("/executar/{chave_tarefa}")
def executar_tarefa(chave_tarefa: str):
    if chave_tarefa not in TAREFAS:
        return RedirectResponse("/", status_code=303)

    nome, funcao = TAREFAS[chave_tarefa]
    inicio = time.perf_counter()
    sucesso, mensagem = funcao()
    duracao = time.perf_counter() - inicio

    database.registar_execucao(nome, sucesso, mensagem, duracao)
    return RedirectResponse("/historico", status_code=303)


@app.get("/historico")
def pagina_historico(request: Request):
    execucoes = database.obter_historico()
    return templates.TemplateResponse(
        request=request, name="historico.html", context={"execucoes": execucoes}
    )