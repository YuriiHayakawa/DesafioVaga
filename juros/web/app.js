"use strict";

const BRL = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

const el = (sel) => document.querySelector(sel);

function aguardarApi() {
  return new Promise((resolve) => {
    if (window.pywebview && window.pywebview.api) return resolve();
    window.addEventListener("pywebviewready", () => resolve(), { once: true });
  });
}

function formatarDataBR(iso) {
  const [a, m, d] = iso.split("-");
  return `${d}/${m}/${a}`;
}

async function iniciar() {
  const p = await window.pywebview.api.parametros();
  el("#hoje").textContent = "Hoje: " + formatarDataBR(p.hoje);
  el("#regra").textContent =
    `Multa de ${(p.taxa_diaria * 100).toLocaleString("pt-BR")}% ao dia sobre o valor.`;
  // Sugere o vencimento como a data de hoje.
  el("#vencimento").value = p.hoje;
}

async function calcular() {
  const erro = el("#erro");
  erro.textContent = "";

  const valor = el("#valor").value;
  const vencimento = el("#vencimento").value;

  if (!valor) {
    erro.textContent = "Informe o valor.";
    return;
  }
  if (!vencimento) {
    erro.textContent = "Informe a data de vencimento.";
    return;
  }

  const r = await window.pywebview.api.calcular(valor, vencimento);
  if (!r.ok) {
    erro.textContent = "⚠ " + r.erro;
    return;
  }
  render(r.resultado);
}

function render(res) {
  el("#situacao").innerHTML = res.em_atraso
    ? `<span class="badge atraso">${res.dias_atraso} dia(s) em atraso</span>`
    : `<span class="badge ok">Em dia</span>`;

  el("#resultado").innerHTML = `
    <div class="total-bloco">
      <div class="rotulo">Total a pagar</div>
      <div class="valor">${BRL.format(res.total)}</div>
    </div>
    <div class="linhas">
      <div class="linha">
        <span class="rot">Valor original</span>
        <span class="val">${BRL.format(res.valor_original)}</span>
      </div>
      <div class="linha">
        <span class="rot">Vencimento</span>
        <span class="val">${res.data_vencimento}</span>
      </div>
      <div class="linha">
        <span class="rot">Data de referência</span>
        <span class="val">${res.data_referencia}</span>
      </div>
      <div class="linha">
        <span class="rot">Dias em atraso</span>
        <span class="val">${res.dias_atraso}</span>
      </div>
      <div class="linha">
        <span class="rot">Taxa</span>
        <span class="val">${(res.taxa_diaria * 100).toLocaleString("pt-BR")}% ao dia</span>
      </div>
      <div class="linha juros">
        <span class="rot">Juros (multa)</span>
        <span class="val">${BRL.format(res.juros)}</span>
      </div>
    </div>`;
}

aguardarApi().then(() => {
  iniciar();
  el("#calcular").addEventListener("click", calcular);
  // Permite calcular pressionando Enter nos campos.
  ["#valor", "#vencimento"].forEach((s) =>
    el(s).addEventListener("keydown", (e) => {
      if (e.key === "Enter") calcular();
    })
  );
});
