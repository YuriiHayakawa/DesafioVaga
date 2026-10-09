from __future__ import annotations

import sys
from pathlib import Path

from src import ServicoEstoque, TipoMovimentacao, carregar_produtos
from src.servico import EstoqueInsuficienteError, ProdutoNaoEncontradoError

BASE_DIR = Path(__file__).resolve().parent


def _mostrar_produtos(servico: ServicoEstoque) -> None:
    print("\n  PRODUTOS EM ESTOQUE")
    print("  " + "-" * 46)
    for p in servico.produtos:
        print(f"  [{p.codigo}] {p.descricao:<32} estoque: {p.estoque:>5}")
    print("  " + "-" * 46)


def _ler_tipo() -> TipoMovimentacao | None:
    valor = input("  Tipo (E=entrada / S=saída): ").strip().lower()
    if valor in ("e", "entrada"):
        return TipoMovimentacao.ENTRADA
    if valor in ("s", "saida", "saída"):
        return TipoMovimentacao.SAIDA
    print("  ! Tipo inválido.")
    return None


def _ler_int(rotulo: str) -> int | None:
    try:
        return int(input(rotulo).strip())
    except ValueError:
        print("  ! Informe um número inteiro.")
        return None


def main(argv: list[str]) -> int:
    arquivo = Path(argv[1]) if len(argv) > 1 else BASE_DIR / "Dados.txt"

    try:
        produtos = carregar_produtos(arquivo)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    servico = ServicoEstoque(produtos)
    print("\n  === CONTROLE DE ESTOQUE ===")
    print("  Digite 'sair' a qualquer momento para encerrar.")

    while True:
        _mostrar_produtos(servico)

        entrada = input("\n  Código do produto a movimentar: ").strip()
        if entrada.lower() == "sair":
            break
        try:
            codigo = int(entrada)
        except ValueError:
            print("  ! Código inválido.")
            continue

        tipo = _ler_tipo()
        if tipo is None:
            continue

        quantidade = _ler_int("  Quantidade: ")
        if quantidade is None:
            continue

        descricao = input("  Descrição da movimentação: ").strip()

        try:
            mov = servico.movimentar(codigo, tipo, quantidade, descricao)
        except (ValueError, EstoqueInsuficienteError, ProdutoNaoEncontradoError) as exc:
            print(f"  ! {exc}")
            continue

        print(
            f"\n  OK  mov #{mov.id} ({mov.tipo.value}) — {mov.produto_descricao}"
            f"\n  >>> Estoque final do produto: {mov.estoque_resultante}"
        )

    print("\n  Encerrado.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
