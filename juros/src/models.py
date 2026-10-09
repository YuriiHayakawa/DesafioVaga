"""Modelos de domínio do cálculo de juros.

Usamos ``Decimal`` para valores monetários de forma a evitar os erros de
arredondamento inerentes ao ``float`` em cálculos financeiros.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ResultadoJuros:
    """Resultado do cálculo de juros por atraso em uma data de referência."""

    valor_original: Decimal
    data_vencimento: date
    data_referencia: date
    dias_atraso: int
    taxa_diaria: Decimal
    juros: Decimal
    total: Decimal

    @property
    def em_atraso(self) -> bool:
        return self.dias_atraso > 0
