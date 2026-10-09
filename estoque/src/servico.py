"""Serviço de orquestração do estoque.

Mantém os produtos em memória, registra movimentações (entrada/saída) com um
identificador único e devolve a quantidade final do produto movimentado.
"""

from __future__ import annotations

from datetime import datetime
from itertools import count
from typing import Iterable

from .models import Movimentacao, Produto, TipoMovimentacao


class ProdutoNaoEncontradoError(Exception):
    """Produto informado não existe no depósito."""


class EstoqueInsuficienteError(Exception):
    """Saída maior do que o estoque disponível."""


class ServicoEstoque:
    """Gerencia o estoque e o histórico de movimentações."""

    def __init__(self, produtos: Iterable[Produto]) -> None:
        self._produtos: dict[int, Produto] = {p.codigo: p for p in produtos}
        self._movimentacoes: list[Movimentacao] = []
        # Gerador de identificadores únicos e sequenciais (1, 2, 3, ...).
        self._proximo_id = count(1)

    # --- consultas -------------------------------------------------------

    @property
    def produtos(self) -> list[Produto]:
        return list(self._produtos.values())

    @property
    def movimentacoes(self) -> list[Movimentacao]:
        """Histórico, da movimentação mais recente para a mais antiga."""
        return list(reversed(self._movimentacoes))

    def produto(self, codigo: int) -> Produto:
        try:
            return self._produtos[codigo]
        except KeyError:
            raise ProdutoNaoEncontradoError(
                f"Produto de código {codigo} não encontrado."
            ) from None

    # --- comando principal ----------------------------------------------

    def movimentar(
        self,
        codigo: int,
        tipo: TipoMovimentacao,
        quantidade: int,
        descricao: str,
    ) -> Movimentacao:
        """Lança uma movimentação e devolve o registro com o estoque final."""

        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if not descricao or not descricao.strip():
            raise ValueError("Informe uma descrição para a movimentação.")

        produto = self.produto(codigo)
        novo_estoque = produto.estoque + tipo.sinal * quantidade

        if novo_estoque < 0:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para '{produto.descricao}': "
                f"disponível {produto.estoque}, saída solicitada {quantidade}."
            )

        produto.estoque = novo_estoque
        movimentacao = Movimentacao(
            id=next(self._proximo_id),
            produto_codigo=produto.codigo,
            produto_descricao=produto.descricao,
            tipo=tipo,
            quantidade=quantidade,
            descricao=descricao.strip(),
            estoque_resultante=novo_estoque,
            criada_em=datetime.now(),
        )
        self._movimentacoes.append(movimentacao)
        return movimentacao
