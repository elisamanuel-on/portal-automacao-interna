# Portal de Automação Interna

Um pequeno portal web que dispara e regista automações internas — uma demonstração de RPA (automação de processos repetitivos) ligada a um portal de gestão, no âmbito da área de desenvolvimento e automação de processos internos.

**Demonstração ao vivo:** https://portal-automacao-interna.onrender.com

## O que faz

O portal expõe três automações através de um botão "Executar", e guarda um histórico de cada execução (tarefa, resultado, duração e data/hora):

- **Organizar Ficheiros** — move ficheiros de uma pasta para subpastas por tipo (documentos, imagens, dados).
- **Gerar Relatório** — lê um ficheiro CSV de vendas e produz um resumo em texto (total e número de linhas).
- **Fazer Backup** — comprime uma pasta num `.zip` com data e hora no nome.

## Agendamento automático (cron)

Além de correrem por clique no portal, as automações também podem correr sozinhas, sem qualquer intervenção manual, através do agendador de tarefas do Linux (`cron`).

O script `scripts/executar_agendado.py` corre a automação de backup e regista o resultado na mesma base de dados do portal — por isso uma execução agendada aparece no histórico exatamente como uma execução manual.

Exemplo de agendamento (todos os dias às 20h):

    crontab -e

    0 20 * * * cd /caminho/para/o/projeto && /caminho/para/o/projeto/venv/bin/python scripts/executar_agendado.py >> /caminho/para/o/projeto/logs/cron.log 2>&1

## Stack técnica

- Python 3.14
- FastAPI — backend e rotas
- Jinja2 — templates HTML
- SQLite — histórico de execuções
- pytest — testes automáticos
- cron — agendamento automático no Ubuntu
- Ubuntu (WSL2) — ambiente de desenvolvimento
- Render — alojamento da demonstração ao vivo

## Como correr localmente

    git clone https://github.com/elisamanuel-on/portal-automacao-interna.git
    cd portal-automacao-interna
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements-dev.txt
    uvicorn app.main:app --reload

Depois abre http://localhost:8000 no browser.

## Como correr os testes

    pytest -v

## Nota sobre o histórico

Esta é uma demonstração de portfólio, alojada num serviço gratuito. O disco não é permanente, por isso o histórico de execuções pode reiniciar periodicamente (por exemplo, quando o serviço "adormece" por inatividade). As automações continuam a funcionar normalmente.

## Próximos passos

- Dois templates de sites para freelance (vitrine + interativo).

## Autora

Elisama Manuel