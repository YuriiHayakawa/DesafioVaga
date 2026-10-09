"use strict";

const BRL = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const PCT = new Intl.NumberFormat("pt-BR", {
  style: "percent",
  minimumFractionDigits: 0,
  maximumFractionDigits: 2,
});

const el = (sel) => document.querySelector(sel);

/** Aguarda a API do pywebview ficar disponível. */
function aguardarApi() {
  return new Promise((resolve) => {
    if (window.pywebview && window.pywebview.api) return resolve();
    window.addEventListener("pywebviewready", () => resolve(), { once: true });
  });
}

async function carregar() {
  const status = el("#status");
  status.textContent = "Carregando dados…";
  status.classList.remove("erro");

  try {
    const dados = await window.pywebview.api.carregar_dashboard();
    if (!dados.ok) {
      status.textContent = "Erro: " + dados.erro;
      status.classList.add("erro");
      return;
    }
    renderKpis(dados.resumo_geral);
    renderFaixas(dados.faixas);
    renderRanking(dados.vendedores);
    renderVendedores(dados.vendedores);

    const g = dados.resumo_geral;
    status.textContent = `${g.quantidade_vendas} vendas · ${g.quantidade_vendedores} vendedores processados`;
  } catch (e) {
    status.textContent = "Falha ao comunicar com o backend: " + e;
    status.classList.add("erro");
  }
}

function renderKpis(g) {
  const cards = [
    { rotulo: "Total vendido", valor: BRL.format(g.total_vendido) },
    {
      rotulo: "Total de comissões",
      valor: BRL.format(g.total_comissao),
      destaque: true,
    },
    { rotulo: "Vendas", valor: String(g.quantidade_vendas) },
    { rotulo: "Vendedores", valor: String(g.quantidade_vendedores) },
  ];
  el("#kpis").innerHTML = cards
    .map(
      (c, i) => `
      <div class="kpi ${c.destaque ? "destaque" : ""}" style="animation-delay:${i * 60}ms">
        <div class="rotulo">${c.rotulo}</div>
        <div class="valor">${c.valor}</div>
      </div>`
    )
    .join("");
}

function renderFaixas(faixas) {
  el("#faixas").innerHTML = faixas
    .map(
      (f) => `
      <li>
        <span>${f.descricao}</span>
        <span class="pct">${PCT.format(f.percentual)}</span>
      </li>`
    )
    .join("");
}

function renderRanking(vendedores) {
  const max = Math.max(...vendedores.map((v) => v.total_comissao), 1);
  el("#ranking").innerHTML = vendedores
    .map(
      (v) => `
      <div class="barra-linha">
        <span class="barra-nome" title="${v.vendedor}">${v.vendedor}</span>
        <div class="barra-trilho">
          <div class="barra-preenchida" data-w="${(v.total_comissao / max) * 100}"></div>
        </div>
        <span class="barra-valor">${BRL.format(v.total_comissao)}</span>
      </div>`
    )
    .join("");

  // Dispara a animação de largura após o layout.
  requestAnimationFrame(() => {
    document.querySelectorAll(".barra-preenchida").forEach((b) => {
      b.style.width = b.dataset.w + "%";
    });
  });
}

function renderVendedores(vendedores) {
  el("#vendedores").innerHTML = vendedores
    .map((v) => {
      const linhas = v.vendas
        .map((s) => {
          const zero = s.comissao === 0 ? "zero" : "";
          return `
            <tr>
              <td>${BRL.format(s.valor)}</td>
              <td class="${zero}">${PCT.format(s.percentual)}</td>
              <td class="${zero}">${BRL.format(s.comissao)}</td>
            </tr>`;
        })
        .join("");

      return `
        <details class="vendedor">
          <summary>
            <div>
              <div class="nome">${v.vendedor}</div>
              <div class="sub">${v.quantidade_vendas} vendas · ticket ${BRL.format(v.ticket_medio)}</div>
            </div>
            <div class="comissao-total">${BRL.format(v.total_comissao)}</div>
          </summary>
          <table class="tabela">
            <thead>
              <tr><th>Venda</th><th>%</th><th>Comissão</th></tr>
            </thead>
            <tbody>${linhas}</tbody>
          </table>
        </details>`;
    })
    .join("");
}

aguardarApi().then(() => {
  carregar();
  el("#recarregar").addEventListener("click", carregar);
});
