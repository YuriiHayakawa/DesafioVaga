from __future__ import annotations

import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from src import ServicoJuros
from src.models import ResultadoJuros


def _brl(valor: Decimal) -> str:
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def _ler_valor(texto: str) -> Decimal:
    return Decimal(texto.strip().replace(".", "").replace(",", "."))


def _ler_data(texto: str) -> date:
    texto = texto.strip()
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).date()
        except ValueError:
            continue
    raise ValueError("Data inválida (use DD/MM/AAAA).")


def _imprimir(r: ResultadoJuros) -> None:
    print("\n  === CÁLCULO DE JUROS ===")
    print(f"  Valor original ....: {_brl(r.valor_original)}")
    print(f"  Vencimento ........: {r.data_vencimento.strftime('%d/%m/%Y')}")
    print(f"  Data de hoje ......: {r.data_referencia.strftime('%d/%m/%Y')}")
    print(f"  Dias em atraso ....: {r.dias_atraso}")
    print(f"  Taxa ..............: {r.taxa_diaria:.1%} ao dia")
    print(f"  Juros .............: {_brl(r.juros)}")
    print(f"  TOTAL A PAGAR .....: {_brl(r.total)}\n")


def main(argv: list[str]) -> int:
    servico = ServicoJuros()

    try:
        if len(argv) >= 3:
            valor = _ler_valor(argv[1])
            vencimento = _ler_data(argv[2])
        else:
            valor = _ler_valor(input("  Valor (R$): "))
            vencimento = _ler_data(input("  Data de vencimento (DD/MM/AAAA): "))

        resultado = servico.calcular(valor, vencimento)
    except (InvalidOperation, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    _imprimir(resultado)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
