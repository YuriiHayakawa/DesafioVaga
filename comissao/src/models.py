"""Modelos de domínio.

Usamos ``Decimal`` para valores monetários de forma a evitar os erros de
arredondamento inerentes ao ``float`` em cálculos financeiros.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Venda:
    """Uma venda individual registrada por um vendedor."""

    vendedor: str
    valor: Decimal

    def __post_init__(self) -> None:
        if not self.vendedor or not self.vendedor.strip():
            raise ValueError("A venda precisa de um vendedor identificado.")
        if self.valor < 0:
            raise ValueError("O valor da venda não pode ser negativo.")


@dataclass(frozen=True, slots=True)
class ComissaoVenda:
    """Resultado do cálculo de comissão para uma única venda."""

    venda: Venda
    percentual: Decimal
    comissao: Decimal


@dataclass(slots=True)
class ResumoVendedor:
    """Totais consolidados de um vendedor."""

    vendedor: str
    total_vendido: Decimal = Decimal("0")
    total_comissao: Decimal = Decimal("0")
    quantidade_vendas: int = 0
    comissoes: list[ComissaoVenda] = field(default_factory=list)

    @property
    def ticket_medio(self) -> Decimal:
        if self.quantidade_vendas == 0:
            return Decimal("0")
        return self.total_vendido / self.quantidade_vendas
