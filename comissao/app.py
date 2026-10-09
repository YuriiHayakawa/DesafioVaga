from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import webview

from src import ServicoComissao, carregar_vendas
from src.models import ResumoVendedor
from src.regras import TABELA_PADRAO

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_DADOS = BASE_DIR / "Dados.txt"
INDEX_HTML = BASE_DIR / "web" / "index.html"


def _num(valor: Decimal) -> float:
    """Converte Decimal para float apenas na fronteira de apresentação."""
    return float(valor)


def _resumo_para_dict(resumo: ResumoVendedor) -> dict:
    return {
        "vendedor": resumo.vendedor,
        "total_vendido": _num(resumo.total_vendido),
        "total_comissao": _num(resumo.total_comissao),
        "quantidade_vendas": resumo.quantidade_vendas,
        "ticket_medio": _num(resumo.ticket_medio),
        "vendas": [
            {
                "valor": _num(c.venda.valor),
                "percentual": _num(c.percentual),
                "comissao": _num(c.comissao),
            }
            for c in resumo.comissoes
        ],
    }


class Api:
    """Ponte entre o Python e o front-end."""

    def __init__(self, arquivo_dados: Path) -> None:
        self._arquivo = arquivo_dados
        self._servico = ServicoComissao(TABELA_PADRAO)

    def carregar_dashboard(self) -> dict:
        """Lê os dados, calcula e devolve o payload completo do dashboard."""
        try:
            vendas = carregar_vendas(self._arquivo)
            resumos = self._servico.consolidar(vendas)
        except (FileNotFoundError, ValueError) as exc:
            return {"ok": False, "erro": str(exc)}

        total_comissao = self._servico.total_comissao(resumos)
        total_vendido = sum((r.total_vendido for r in resumos), Decimal("0"))

        return {
            "ok": True,
            "resumo_geral": {
                "total_vendido": _num(total_vendido),
                "total_comissao": _num(total_comissao),
                "quantidade_vendas": sum(r.quantidade_vendas for r in resumos),
                "quantidade_vendedores": len(resumos),
            },
            "faixas": [
                {"descricao": f.descricao, "percentual": _num(f.percentual)}
                for f in TABELA_PADRAO.faixas
            ],
            "vendedores": [_resumo_para_dict(r) for r in resumos],
        }


def main() -> None:
    api = Api(ARQUIVO_DADOS)
    webview.create_window(
        title="Comissões — Time Comercial",
        url=str(INDEX_HTML),
        js_api=api,
        width=1120,
        height=820,
        min_size=(880, 640),
    )
    webview.start()


if __name__ == "__main__":
    main()
