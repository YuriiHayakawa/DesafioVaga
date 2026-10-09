from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

import webview

from src import ServicoJuros, TAXA_DIARIA_PADRAO
from src.models import ResultadoJuros

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML = BASE_DIR / "web" / "index.html"


def _resultado_dict(r: ResultadoJuros) -> dict:
    return {
        "valor_original": float(r.valor_original),
        "data_vencimento": r.data_vencimento.strftime("%d/%m/%Y"),
        "data_referencia": r.data_referencia.strftime("%d/%m/%Y"),
        "dias_atraso": r.dias_atraso,
        "taxa_diaria": float(r.taxa_diaria),
        "juros": float(r.juros),
        "total": float(r.total),
        "em_atraso": r.em_atraso,
    }


class Api:
    """Ponte entre o Python e o front-end."""

    def __init__(self) -> None:
        self._servico = ServicoJuros()

    def parametros(self) -> dict:
        """Dados iniciais para a interface (data de hoje e a taxa)."""
        return {
            "hoje": date.today().isoformat(),
            "taxa_diaria": float(TAXA_DIARIA_PADRAO),
        }

    def calcular(self, valor: str, vencimento: str) -> dict:
        """Calcula os juros. ``vencimento`` no formato ISO (YYYY-MM-DD)."""
        try:
            valor_decimal = Decimal(str(valor).replace(",", "."))
        except (InvalidOperation, ValueError):
            return {"ok": False, "erro": "Informe um valor numérico válido."}

        try:
            data_venc = date.fromisoformat(vencimento)
        except (ValueError, TypeError):
            return {"ok": False, "erro": "Informe uma data de vencimento válida."}

        try:
            resultado = self._servico.calcular(valor_decimal, data_venc)
        except ValueError as exc:
            return {"ok": False, "erro": str(exc)}

        return {"ok": True, "resultado": _resultado_dict(resultado)}


def main() -> None:
    webview.create_window(
        title="Cálculo de Juros por Atraso",
        url=str(INDEX_HTML),
        js_api=Api(),
        width=960,
        height=760,
        min_size=(820, 620),
    )
    webview.start()


if __name__ == "__main__":
    main()
