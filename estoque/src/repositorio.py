"""Leitura e normalização da fonte de dados dos produtos.

Assim como no outro módulo, o ``Dados.txt`` guarda um JSON cujas aspas foram
escapadas como entidades HTML (``&quot;``); desescapamos antes de interpretar.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

from .models import Produto


def carregar_produtos(caminho: str | Path) -> list[Produto]:
    """Lê o arquivo e devolve a lista de produtos com o estoque inicial."""

    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {caminho}")

    return _interpretar(caminho.read_text(encoding="utf-8"))


def _interpretar(conteudo: str) -> list[Produto]:
    texto = html.unescape(conteudo)
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido na fonte de dados: {exc}") from exc

    registros = dados.get("estoque") if isinstance(dados, dict) else None
    if not isinstance(registros, list):
        raise ValueError("Esperava um objeto com a chave 'estoque' contendo uma lista.")

    return [_para_produto(r, i) for i, r in enumerate(registros, start=1)]


def _para_produto(registro: object, indice: int) -> Produto:
    if not isinstance(registro, dict):
        raise ValueError(f"Registro #{indice} inválido: esperava um objeto.")

    try:
        codigo = int(registro["codigoProduto"])
        descricao = str(registro["descricaoProduto"]).strip()
        estoque = int(registro["estoque"])
    except KeyError as exc:
        raise ValueError(f"Registro #{indice} sem o campo {exc}.") from exc
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Registro #{indice} com dados inválidos: {exc}") from exc

    return Produto(codigo=codigo, descricao=descricao, estoque=estoque)
