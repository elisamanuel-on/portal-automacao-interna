"""
Testes para as automações do portal (app/automacoes.py).
"""
import zipfile
from pathlib import Path

from app import automacoes


def test_organizar_ficheiros_move_por_tipo(tmp_path):
    (tmp_path / "fatura.pdf").write_text("conteudo")
    (tmp_path / "foto.jpg").write_text("conteudo")
    (tmp_path / "dados.csv").write_text("produto,valor\n")

    sucesso, mensagem = automacoes.organizar_ficheiros(tmp_path)

    assert sucesso is True
    assert "3 ficheiro(s)" in mensagem
    assert (tmp_path / "documentos" / "fatura.pdf").exists()
    assert (tmp_path / "imagens" / "foto.jpg").exists()
    assert (tmp_path / "dados" / "dados.csv").exists()


def test_organizar_ficheiros_pasta_inexistente(tmp_path):
    pasta_falsa = tmp_path / "nao_existe"

    sucesso, mensagem = automacoes.organizar_ficheiros(pasta_falsa)

    assert sucesso is False
    assert "não existe" in mensagem


def test_gerar_relatorio_soma_valores(tmp_path):
    (tmp_path / "vendas.csv").write_text(
        "produto,valor\nCaneta,10.50\nCaderno,5.25\n", encoding="utf-8"
    )

    sucesso, mensagem = automacoes.gerar_relatorio(tmp_path, "vendas.csv")

    assert sucesso is True
    assert "2 linha(s)" in mensagem
    assert "15.75" in mensagem
    assert (tmp_path / "relatorio.txt").exists()


def test_gerar_relatorio_encontra_csv_na_subpasta_dados(tmp_path):
    """
    Simula o cenário em que 'Organizar Ficheiros' já correu antes e
    moveu o vendas.csv para dentro de 'dados/'. O relatório deve
    continuar a encontrá-lo e a ser escrito na pasta principal.
    """
    pasta_dados = tmp_path / "dados"
    pasta_dados.mkdir()
    (pasta_dados / "vendas.csv").write_text(
        "produto,valor\nCaneta,10.50\n", encoding="utf-8"
    )

    sucesso, mensagem = automacoes.gerar_relatorio(tmp_path, "vendas.csv")

    assert sucesso is True
    assert "1 linha(s)" in mensagem
    assert (tmp_path / "relatorio.txt").exists()
    assert not (pasta_dados / "relatorio.txt").exists()


def test_fazer_backup_cria_zip(tmp_path):
    (tmp_path / "ficheiro.txt").write_text("conteudo")

    sucesso, mensagem = automacoes.fazer_backup(tmp_path)

    assert sucesso is True
    assert "Backup criado em" in mensagem
    caminho_zip = mensagem.split("Backup criado em ")[1].rstrip(".")
    assert Path(caminho_zip).exists()
    assert zipfile.is_zipfile(caminho_zip)