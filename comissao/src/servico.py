"""Serviço de orquestração: aplica as regras e consolida os resultados."""

from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from .models import ComissaoVenda, ResumoVendedor, Venda
from .regras import TABELA_PADRAO, TabelaComissao


class ServicoComissao:
    """Calcula comissões por venda e consolida totais por vendedor."""

    def __init__(self, tabela: TabelaComissao | None = None) -> None:
        self._tabela = tabela or TABELA_PADRAO

    def comissao_da_venda(self, venda: Venda) -> ComissaoVenda:
        percentual = self._tabela.percentual_para(venda.valor)
        comissao = self._tabela.calcular_comissao(venda.valor)
        return ComissaoVenda(venda=venda, percentual=percentual, comissao=comissao)

    def consolidar(self, vendas: Iterable[Venda]) -> list[ResumoVendedor]:
        """Agrupa por vendedor e devolve os resumos ordenados por comissão."""

        resumos: dict[str, ResumoVendedor] = {}
        for venda in vendas:
            resumo = resumos.setdefault(venda.vendedor, ResumoVendedor(venda.vendedor))
            item = self.comissao_da_venda(venda)

            resumo.comissoes.append(item)
            resumo.quantidade_vendas += 1
            resumo.total_vendido += venda.valor
            resumo.total_comissao += item.comissao

        return sorted(
            resumos.values(),
            key=lambda r: r.total_comissao,
            reverse=True,
        )

    @staticmethod
    def total_comissao(resumos: Iterable[ResumoVendedor]) -> Decimal:
        return sum((r.total_comissao for r in resumos), Decimal("0"))
