# Desafio — Três Programas em Python

Três programinhas independentes, cada um em sua pasta, seguindo o mesmo padrão:
código Python simples e bem estruturado (separado em camadas no pacote `src/`)
e uma interface desktop feita com **pywebview** (HTML + CSS + JS locais, sem
dependências externas — roda offline).

| Pasta | Programa | O que faz |
| ----- | -------- | --------- |
| [`comissao/`](comissao/) | Comissões | Lê as vendas e calcula a comissão de cada vendedor. |
| [`estoque/`](estoque/)   | Estoque   | Lança movimentações (entrada/saída) e controla o estoque. |
| [`juros/`](juros/)       | Juros     | Calcula juros por atraso a partir de um valor e do vencimento. |

## Como executar

Cada programa roda pelo seu próprio `main.py`. Dentro da pasta do programa:

```bash
pip install -r requirements.txt   # pywebview

python main.py        # abre o painel visual (pywebview)
python main.py --cli  # versão em terminal
```

---

## 1. Comissões — `comissao/`

Lê as vendas de um time comercial (`Dados.txt`) e calcula a comissão por venda,
consolidando o total de cada vendedor num painel com ranking.

**Regras de comissão:**

| Valor da venda           | Comissão |
| ------------------------ | -------- |
| abaixo de R$ 100,00      | 0%       |
| de R$ 100,00 a R$ 499,99 | 1%       |
| a partir de R$ 500,00    | 5%       |

A interface mostra KPIs (total vendido, total de comissões), ranking por
vendedor e o detalhamento venda a venda.

## 2. Estoque — `estoque/`

Lança movimentações de estoque dos produtos de `Dados.txt`, dando entrada ou
saída de mercadoria no depósito.

Cada movimentação tem:

- **Identificador único** — número sequencial gerado automaticamente.
- **Descrição** — texto que identifica o tipo da movimentação (ex.: "Compra
  fornecedor", "Venda balcão").

Ao final de cada movimentação o sistema retorna a **quantidade final do estoque**
do produto movimentado. Saídas maiores que o estoque disponível são bloqueadas.
O estoque vive em memória durante a execução; o botão "Reiniciar" recarrega os
valores originais do arquivo.

## 3. Juros por Atraso — `juros/`

A partir de um **valor** e de uma **data de vencimento**, calcula os juros na
data de hoje. Diferente dos outros dois, **não tem base de dados** — os dados
vêm direto da interface.

**Regra:** multa de **2,5% ao dia** sobre o valor, por dia de atraso.

```
juros = valor × 2,5% × dias_de_atraso
total = valor + juros
```

Sem atraso (vencimento futuro ou hoje), não há juros.

---

## Padrões adotados

- **Arquitetura em camadas** no pacote `src/` de cada programa
  (`models` → `repositorio` → `servico`), mantendo a regra de negócio isolada
  da leitura de dados e da interface.
- **`Decimal`** para valores monetários, evitando erros de arredondamento do
  `float`; arredondamento ao centavo com `ROUND_HALF_UP`.
- **Fonte de dados:** os arquivos `Dados.txt` guardam um JSON cujas aspas vêm
  escapadas como entidades HTML (`&quot;`); o repositório faz `html.unescape`
  antes do `json.loads`.
- **Interface pywebview** com `main.py` como ponto de entrada único e um modo
  `--cli` alternativo para rodar sem abrir a janela.

## Requisitos

- Python 3.11+
- `pywebview` — ver `requirements.txt` de cada programa.
