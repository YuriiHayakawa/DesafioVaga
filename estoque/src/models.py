"""Modelos de domínio do controle de estoque."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TipoMovimentacao(str, Enum):
    """Tipo de movimentação no depósito."""

    ENTRADA = "entrada"
    SAIDA = "saida"

    @property
    def sinal(self) -> int:
        """+1 soma ao estoque (entrada), -1 subtrai (saída)."""
        return 1 if self is TipoMovimentacao.ENTRADA else -1


@dataclass(slots=True)
class Produto:
    """Produto do depósito e sua quantidade atual em estoque."""

    codigo: int
    descricao: str
    estoque: int

    def __post_init__(self) -> None:
        if self.estoque < 0:
            raise ValueError("O estoque inicial não pode ser negativo.")


@dataclass(frozen=True, slots=True)
class Movimentacao:
    """Registro imutável de uma movimentação de estoque.

    Cada movimentação tem um identificador único (``id``) e uma ``descricao``
    que identifica o tipo da movimentação realizada.
    """

    id: int
    produto_codigo: int
    produto_descricao: str
    tipo: TipoMovimentacao
    quantidade: int
    descricao: str
    estoque_resultante: int
    criada_em: datetime
