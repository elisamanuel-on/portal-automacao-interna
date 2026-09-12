# Portal de Automação Interna

Um pequeno portal web que dispara e regista automações internas — uma demonstração de RPA (automação de processos repetitivos) ligada a um portal de gestão, no âmbito da área de desenvolvimento e automação de processos internos.

## O que faz

O portal expõe três automações através de um botão "Executar", e guarda um histórico de cada execução (tarefa, resultado, duração e data/hora):

- **Organizar Ficheiros** — move ficheiros de uma pasta para subpastas por tipo (documentos, imagens, dados).
- **Gerar Relatório** — lê um ficheiro CSV de vendas e produz um resumo em texto (total e número de linhas).
- **Fazer Backup** — comprime uma pasta num `.zip` com data e hora no nome.

## Stack técnica

- Python 3.14
- FastAPI — backend e rotas
- Jinja2 — templates HTML
- SQLite — histórico de execuções
- pytest — testes automáticos
- Ubuntu (WSL2) — ambiente de desenvolvimento

## Como correr localmente

    git clone https://github.com/<o-teu-utilizador>/portal-automacao-interna.git
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

- Agendamento automático das automações via cron no Ubuntu.
- Dois templates de sites para freelance (vitrine + interativo).

## Autora

Elisama Manuel