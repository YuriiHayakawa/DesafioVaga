# 🐍 Desafio — Três Programas em Python

Três aplicações independentes desenvolvidas em **Python**, com foco em organização de código, separação de responsabilidades e interfaces desktop modernas utilizando **pywebview**.

Cada programa possui sua própria estrutura, regras de negócio e interface gráfica, além de oferecer uma versão alternativa via terminal (CLI).

## 📂 Projetos

| Projeto                                                                        | Descrição                  | Funcionalidades                                                                  |
| :----------------------------------------------------------------------------- | :------------------------- | :------------------------------------------------------------------------------- |
| [`comissao/`](https://github.com/YuriiHayakawa/DesafioVaga/tree/main/comissao) | 💰 **Comissões**           | Cálculo de comissões, consolidação por vendedor e ranking de desempenho.         |
| [`estoque/`](https://github.com/YuriiHayakawa/DesafioVaga/tree/main/estoque)   | 📦 **Controle de Estoque** | Registro de entradas e saídas, controle de saldo e validação de disponibilidade. |
| [`juros/`](https://github.com/YuriiHayakawa/DesafioVaga/tree/main/juros)       | 🧮 **Juros por Atraso**    | Cálculo de juros com base no valor original e nos dias de atraso.                |

---

## 🚀 Como executar

### Pré-requisitos

* Python 3.11 ou superior
* pip

### Instalação e execução

Entre na pasta do programa desejado e instale as dependências:

```bash
pip install -r requirements.txt
```

**Interface gráfica (pywebview):**

```bash
python main.py
```

**Modo terminal (CLI):**

```bash
python main.py --cli
```

> Cada aplicação possui seu próprio `main.py` e arquivo `requirements.txt`, permitindo a execução independente dos projetos.

---

## 💰 1. Comissões

Calcula as comissões de uma equipe comercial a partir das vendas armazenadas em `Dados.txt`.

### Regras de comissão

| Valor da venda           | Taxa de comissão |
| :----------------------- | :--------------: |
| Abaixo de R$ 100,00      |        0%        |
| De R$ 100,00 a R$ 499,99 |        1%        |
| A partir de R$ 500,00    |        5%        |

### Funcionalidades

* Leitura e processamento dos dados de vendas.
* Cálculo individual da comissão de cada venda.
* Consolidação das vendas e comissões por vendedor.
* Ranking de vendedores.
* Painel visual com indicadores de desempenho:

  * Total vendido.
  * Total de comissões.
  * Detalhamento das vendas.

---

## 📦 2. Controle de Estoque

Permite registrar movimentações de entrada e saída de mercadorias, mantendo o saldo atualizado de cada produto.

### Funcionalidades

* Carregamento dos produtos a partir de `Dados.txt`.
* Registro de entradas e saídas de estoque.
* Geração automática de identificadores sequenciais para as movimentações.
* Descrição de cada operação, como *Compra fornecedor* ou *Venda balcão*.
* Atualização e retorno da quantidade final do produto movimentado.
* Bloqueio de saídas superiores à quantidade disponível.
* Opção **Reiniciar** para restaurar os saldos originais carregados do arquivo.

> **Observação:** as movimentações são mantidas em memória durante a execução. Ao reiniciar o sistema, os saldos retornam aos valores originais de `Dados.txt`.

---

## 🧮 3. Juros por Atraso

Calcula os juros de uma dívida com base no valor informado e na data de vencimento.

Diferentemente dos outros programas, esta aplicação não utiliza arquivo de dados: todas as informações são fornecidas diretamente pela interface.

### Regra de cálculo

A taxa de juros é de **2,5% ao dia**, aplicada sobre o valor original para cada dia de atraso.

**Fórmulas:**

```text
Juros = Valor × 0,025 × Dias de atraso

Total = Valor + Juros
```

### Comportamento

* Recebe o valor original e a data de vencimento.
* Calcula automaticamente os dias de atraso.
* Aplica a taxa diária de 2,5%.
* Apresenta o valor dos juros e o total atualizado.
* Não aplica juros quando o vencimento ocorre na data atual ou no futuro.

---

## 🏗️ Arquitetura e organização

Os três projetos seguem o mesmo padrão de organização, com separação de responsabilidades em camadas dentro do pacote `src/`.

```text
projeto/
├── main.py
├── requirements.txt
├── Dados.txt              # Quando aplicável
├── src/
│   ├── models/            # Modelos e entidades
│   ├── repositorio/       # Acesso e leitura dos dados
│   └── servico/           # Regras de negócio
└── interface/             # HTML, CSS e JavaScript
```

*Estrutura ilustrativa: os nomes e arquivos específicos podem variar conforme cada aplicação.*

### Tecnologias e decisões técnicas

| Tecnologia / Recurso       | Aplicação                                               |
| :------------------------- | :------------------------------------------------------ |
| **Python 3.11+**           | Lógica de negócio e processamento dos dados.            |
| **pywebview**              | Integração entre Python e a interface desktop.          |
| **HTML, CSS e JavaScript** | Construção das interfaces gráficas locais.              |
| **Decimal**                | Manipulação de valores monetários com precisão decimal. |
| **ROUND_HALF_UP**          | Arredondamento monetário convencional ao centavo.       |
| **JSON**                   | Organização dos dados armazenados nos arquivos.         |
| **CLI**                    | Alternativa para execução sem interface gráfica.        |

### Padrões adotados

* **Separação de responsabilidades:** modelos, repositórios e serviços organizados em camadas.
* **Regras de negócio isoladas:** cálculos e validações separados da interface gráfica.
* **Precisão monetária:** utilização de `Decimal` em vez de `float`, com arredondamento por `ROUND_HALF_UP`.
* **Tratamento dos dados:** aplicação de `html.unescape` antes de `json.loads` para processar JSON com aspas escapadas como entidades HTML (`&quot;`).
* **Execução independente:** cada programa possui seu próprio ponto de entrada e suas dependências.
* **Interface offline:** arquivos HTML, CSS e JavaScript locais, sem dependências externas de frontend.

---

## 📋 Requisitos

* Python 3.11 ou superior.
* `pywebview`, listado no `requirements.txt` de cada programa.
* Ambiente desktop compatível com o backend gráfico utilizado pelo pywebview.

## 🎯 Objetivo do desafio

Demonstrar a implementação de pequenas aplicações em Python com foco em **organização de código, lógica de negócio, manipulação de dados, precisão em cálculos monetários e desenvolvimento de interfaces desktop**.

---

Desenvolvido como parte de um desafio técnico.
