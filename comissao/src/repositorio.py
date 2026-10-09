"""Leitura e normalização da fonte de dados de vendas.

O arquivo ``Dados.txt`` guarda um JSON cujas aspas foram escapadas como
entidades HTML (``&quot;``). Por isso desescapamos o conteúdo antes de
interpretar o JSON.
"""

from __future__ import annotations

import html
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from .models import Venda


def carregar_vendas(caminho: str | Path) -> list[Venda]:
    """Lê o arquivo e devolve a lista de vendas validadas."""

    caminho = Path(caminho)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {caminho}")

    bruto = caminho.read_text(encoding="utf-8")
    return _interpretar(bruto)


def _interpretar(conteudo: str) -> list[Venda]:
    texto = html.unescape(conteudo)
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON inválido na fonte de dados: {exc}") from exc

    registros = dados.get("vendas") if isinstance(dados, dict) else None
    if not isinstance(registros, list):
        raise ValueError("Esperava um objeto com a chave 'vendas' contendo uma lista.")

    vendas: list[Venda] = []
    for i, registro in enumerate(registros, start=1):
        vendas.append(_para_venda(registro, i))
    return vendas


def _para_venda(registro: object, indice: int) -> Venda:
    if not isinstance(registro, dict):
        raise ValueError(f"Registro #{indice} inválido: esperava um objeto.")

    vendedor = registro.get("vendedor")
    valor = registro.get("valor")
    if vendedor is None or valor is None:
        raise ValueError(f"Registro #{indice} sem 'vendedor' ou 'valor'.")

    try:
        # Passamos por ``str`` para preservar a precisão decimal do número.
        valor_decimal = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Registro #{indice} com valor inválido: {valor!r}") from exc

    return Venda(vendedor=str(vendedor).strip(), valor=valor_decimal)
