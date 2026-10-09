from __future__ import annotations

import sys
from pathlib import Path

from src import ServicoComissao, carregar_vendas

BASE_DIR = Path(__file__).resolve().parent


def _brl(valor) -> str:
    texto = f"{valor:,.2f}"
    # Converte 1,234.56 -> 1.234,56 (padrão brasileiro).
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def main(argv: list[str]) -> int:
    arquivo = Path(argv[1]) if len(argv) > 1 else BASE_DIR / "Dados.txt"

    try:
        vendas = carregar_vendas(arquivo)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    servico = ServicoComissao()
    resumos = servico.consolidar(vendas)

    print("\n  COMISSÕES — TIME COMERCIAL")
    print("  " + "-" * 44)
    for r in resumos:
        print(
            f"  {r.vendedor:<20} "
            f"vendido {_brl(r.total_vendido):>14}   "
            f"comissão {_brl(r.total_comissao):>12}"
        )
    print("  " + "-" * 44)
    print(f"  {'TOTAL':<20} comissões: {_brl(servico.total_comissao(resumos))}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
