"""Regra de negócio e orquestração do cálculo de juros.

Regra:
    * A multa é de 2,5% ao dia sobre o valor, por dia de atraso.
    * Os juros são calculados na data de hoje (ou numa data de referência).
    * Sem atraso (hoje <= vencimento) não há juros.

    juros = valor * taxa_diaria * dias_de_atraso
    total = valor + juros
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from .models import ResultadoJuros

CENTAVO = Decimal("0.01")
TAXA_DIARIA_PADRAO = Decimal("0.025")  # 2,5% ao dia


class ServicoJuros:
    """Calcula os juros por atraso de um título."""

    def __init__(self, taxa_diaria: Decimal = TAXA_DIARIA_PADRAO) -> None:
        if taxa_diaria < 0:
            raise ValueError("A taxa diária não pode ser negativa.")
        self._taxa_diaria = taxa_diaria

    def calcular(
        self,
        valor: Decimal,
        vencimento: date,
        referencia: date | None = None,
    ) -> ResultadoJuros:
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")

        referencia = referencia or date.today()
        dias_atraso = max(0, (referencia - vencimento).days)

        juros = (valor * self._taxa_diaria * dias_atraso).quantize(
            CENTAVO, rounding=ROUND_HALF_UP
        )
        total = (valor + juros).quantize(CENTAVO, rounding=ROUND_HALF_UP)

        return ResultadoJuros(
            valor_original=valor,
            data_vencimento=vencimento,
            data_referencia=referencia,
            dias_atraso=dias_atraso,
            taxa_diaria=self._taxa_diaria,
            juros=juros,
            total=total,
        )
