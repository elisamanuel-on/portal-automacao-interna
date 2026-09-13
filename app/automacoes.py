"""
As três automações do portal. Cada função devolve um tuplo
(sucesso: bool, mensagem: str) a descrever o que aconteceu.
"""
import csv
import shutil
from datetime import datetime
from pathlib import Path

PASTA_TESTE = Path(__file__).resolve().parent.parent / "dados_teste"

CATEGORIAS = {
    ".pdf": "documentos",
    ".docx": "documentos",
    ".txt": "documentos",
    ".jpg": "imagens",
    ".jpeg": "imagens",
    ".png": "imagens",
    ".csv": "dados",
    ".xlsx": "dados",
}


def organizar_ficheiros(pasta: Path = PASTA_TESTE) -> tuple[bool, str]:
    """Organiza os ficheiros de 'pasta' em subpastas, por tipo."""
    pasta = Path(pasta)
    if not pasta.exists():
        return False, f"A pasta {pasta} não existe."

    movidos = 0
    for ficheiro in pasta.iterdir():
        if ficheiro.is_dir():
            continue
        subpasta = CATEGORIAS.get(ficheiro.suffix.lower())
        if subpasta is None:
            continue
        destino = pasta / subpasta
        destino.mkdir(exist_ok=True)
        shutil.move(str(ficheiro), str(destino / ficheiro.name))
        movidos += 1

    return True, f"{movidos} ficheiro(s) organizado(s) em {pasta}."


def gerar_relatorio(pasta: Path = PASTA_TESTE, nome_ficheiro: str = "vendas.csv") -> tuple[bool, str]:
    """
    Lê um CSV (colunas: produto, valor) e gera um resumo em texto.

    O ficheiro pode estar diretamente em 'pasta' ou, se "Organizar
    Ficheiros" já tiver corrido antes, dentro da subpasta "dados"
    (para onde os .csv são movidos). Procuramos nos dois sítios para
    o relatório continuar a funcionar depois da organização.
    """
    pasta = Path(pasta)
    caminho_csv = pasta / nome_ficheiro
    if not caminho_csv.exists():
        alternativa = pasta / "dados" / nome_ficheiro
        if alternativa.exists():
            caminho_csv = alternativa
        else:
            return False, f"O ficheiro {nome_ficheiro} não existe em {pasta} (nem em {pasta / 'dados'})."

    total = 0.0
    linhas = 0
    with open(caminho_csv, newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            total += float(linha["valor"])
            linhas += 1

    # O relatório fica sempre na pasta principal, independentemente de
    # onde o csv foi encontrado.
    caminho_relatorio = pasta / "relatorio.txt"
    with open(caminho_relatorio, "w", encoding="utf-8") as f:
        f.write(f"Relatório gerado em {datetime.now():%Y-%m-%d %H:%M}\n")
        f.write(f"Linhas processadas: {linhas}\n")
        f.write(f"Valor total: {total:.2f}\n")

    return True, f"Relatório gerado com {linhas} linha(s), total {total:.2f}."


def fazer_backup(pasta: Path = PASTA_TESTE) -> tuple[bool, str]:
    """Comprime 'pasta' num .zip com data/hora no nome."""
    pasta = Path(pasta)
    if not pasta.exists():
        return False, f"A pasta {pasta} não existe."

    nome_base = pasta.parent / f"backup_{pasta.name}_{datetime.now():%Y%m%d_%H%M%S}"
    caminho_zip = shutil.make_archive(str(nome_base), "zip", root_dir=pasta)
    return True, f"Backup criado em {caminho_zip}."