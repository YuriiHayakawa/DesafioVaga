from __future__ import annotations

from pathlib import Path

import webview

from src import (
    ServicoEstoque,
    TipoMovimentacao,
    carregar_produtos,
    EstoqueInsuficienteError,
    ProdutoNaoEncontradoError,
)
from src.models import Movimentacao, Produto

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "Dados.txt"
INDEX_HTML = BASE_DIR / "web" / "index.html"


def _produto_dict(p: Produto) -> dict:
    return {"codigo": p.codigo, "descricao": p.descricao, "estoque": p.estoque}


def _movimentacao_dict(m: Movimentacao) -> dict:
    return {
        "id": m.id,
        "produto_codigo": m.produto_codigo,
        "produto_descricao": m.produto_descricao,
        "tipo": m.tipo.value,
        "quantidade": m.quantidade,
        "descricao": m.descricao,
        "estoque_resultante": m.estoque_resultante,
        "criada_em": m.criada_em.strftime("%d/%m/%Y %H:%M:%S"),
    }


class Api:
    """Ponte entre o Python e o front-end."""

    def __init__(self, arquivo_dados: Path) -> None:
        self._arquivo = arquivo_dados
        self._servico: ServicoEstoque | None = None

    def _garantir_servico(self) -> ServicoEstoque:
        if self._servico is None:
            produtos = carregar_produtos(self._arquivo)
            self._servico = ServicoEstoque(produtos)
        return self._servico

    def reiniciar(self) -> dict:
        """Recarrega os produtos do arquivo, descartando as movimentações."""
        self._servico = None
        return self.carregar_estado()

    def carregar_estado(self) -> dict:
        """Devolve produtos e histórico de movimentações."""
        try:
            servico = self._garantir_servico()
        except (FileNotFoundError, ValueError) as exc:
            return {"ok": False, "erro": str(exc)}

        return {
            "ok": True,
            "produtos": [_produto_dict(p) for p in servico.produtos],
            "movimentacoes": [_movimentacao_dict(m) for m in servico.movimentacoes],
        }

    def movimentar(
        self, codigo: int, tipo: str, quantidade: int, descricao: str
    ) -> dict:
        """Registra uma movimentação e devolve o resultado."""
        try:
            servico = self._garantir_servico()
            tipo_mov = TipoMovimentacao(tipo)
            mov = servico.movimentar(int(codigo), tipo_mov, int(quantidade), descricao)
        except ValueError as exc:
            # Cobre tipo inválido, quantidade/descrição inválidas.
            return {"ok": False, "erro": str(exc)}
        except (EstoqueInsuficienteError, ProdutoNaoEncontradoError) as exc:
            return {"ok": False, "erro": str(exc)}

        return {
            "ok": True,
            "movimentacao": _movimentacao_dict(mov),
            "estoque_final": mov.estoque_resultante,
            "produtos": [_produto_dict(p) for p in servico.produtos],
            "movimentacoes": [_movimentacao_dict(m) for m in servico.movimentacoes],
        }


def main() -> None:
    api = Api(ARQUIVO_DADOS)
    webview.create_window(
        title="Controle de Estoque — Depósito",
        url=str(INDEX_HTML),
        js_api=api,
        width=1120,
        height=820,
        min_size=(900, 640),
    )
    webview.start()


if __name__ == "__main__":
    main()
