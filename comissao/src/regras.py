"""Regras de negócio para o cálculo da comissão.

A tabela é orientada a dados (lista de faixas), o que torna trivial ajustar
percentuais ou acrescentar novas faixas sem alterar a lógica de cálculo.

Regras atuais:
    * valor < R$ 100,00          -> 0% (não gera comissão)
    * R$ 100,00 <= valor < 500   -> 1%
    * valor >= R$ 500,00         -> 5%
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Faixa:
    """Faixa de comissão a partir de um valor mínimo (inclusive)."""

    minimo: Decimal
    percentual: Decimal
    descricao: str


class TabelaComissao:
    """Encapsula as faixas e resolve o percentual aplicável a um valor."""

    def __init__(self, faixas: list[Faixa]) -> None:
        if not faixas:
            raise ValueError("A tabela precisa de ao menos uma faixa.")
        # Ordena da maior para a menor para que a primeira faixa cujo mínimo
        # seja atendido já seja a correta.
        self._faixas = sorted(faixas, key=lambda f: f.minimo, reverse=True)

    @property
    def faixas(self) -> list[Faixa]:
        """Faixas ordenadas do menor para o maior valor mínimo."""
        return sorted(self._faixas, key=lambda f: f.minimo)

    def faixa_para(self, valor: Decimal) -> Faixa:
        for faixa in self._faixas:
            if valor >= faixa.minimo:
                return faixa
        # Com uma faixa de mínimo 0 isto nunca é alcançado, mas mantemos
        # a garantia explícita.
        raise ValueError(f"Nenhuma faixa aplicável para o valor {valor}.")

    def percentual_para(self, valor: Decimal) -> Decimal:
        return self.faixa_para(valor).percentual

    def calcular_comissao(self, valor: Decimal) -> Decimal:
        bruto = valor * self.percentual_para(valor)
        return bruto.quantize(CENTAVO, rounding=ROUND_HALF_UP)


TABELA_PADRAO = TabelaComissao(
    [
        Faixa(Decimal("0"), Decimal("0.00"), "Abaixo de R$ 100,00 — sem comissão"),
        Faixa(Decimal("100"), Decimal("0.01"), "De R$ 100,00 a R$ 499,99 — 1%"),
        Faixa(Decimal("500"), Decimal("0.05"), "A partir de R$ 500,00 — 5%"),
    ]
)
