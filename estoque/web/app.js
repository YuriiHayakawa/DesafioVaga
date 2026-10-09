"use strict";

const el = (sel) => document.querySelector(sel);
const LIMITE_BAIXO = 100; // destaca produtos com estoque baixo

let tipoSelecionado = "entrada";

function aguardarApi() {
  return new Promise((resolve) => {
    if (window.pywebview && window.pywebview.api) return resolve();
    window.addEventListener("pywebviewready", () => resolve(), { once: true });
  });
}

async function iniciar() {
  const estado = await window.pywebview.api.carregar_estado();
  const status = el("#status");
  if (!estado.ok) {
    status.textContent = "Erro: " + estado.erro;
    return;
  }
  renderProdutos(estado.produtos);
  preencherSelect(estado.produtos);
  renderHistorico(estado.movimentacoes);
  status.textContent = `${estado.produtos.length} produtos carregados`;
}

function preencherSelect(produtos) {
  el("#produto").innerHTML = produtos
    .map(
      (p) =>
        `<option value="${p.codigo}">[${p.codigo}] ${p.descricao} — ${p.estoque} un</option>`
    )
    .join("");
}

function renderProdutos(produtos, destaqueCodigo) {
  el("#produtos").innerHTML = produtos
    .map((p) => {
      const baixo = p.estoque < LIMITE_BAIXO ? "baixo" : "";
      const flash = p.codigo === destaqueCodigo ? "flash" : "";
      return `
        <div class="produto ${flash}" data-cod="${p.codigo}">
          <div class="cod">Código ${p.codigo}</div>
          <div class="desc">${p.descricao}</div>
          <div><span class="qtd ${baixo}">${p.estoque}</span><span class="unid">un</span></div>
        </div>`;
    })
    .join("");
}

function renderHistorico(movs) {
  const tbody = el("#historico");
  el("#contador").textContent = movs.length
    ? `${movs.length} lançamento(s)`
    : "";

  if (!movs.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="vazio">Nenhuma movimentação lançada ainda.</td></tr>`;
    return;
  }

  tbody.innerHTML = movs
    .map(
      (m) => `
      <tr>
        <td>${m.id}</td>
        <td>${m.criada_em}</td>
        <td class="l">${m.produto_descricao}</td>
        <td><span class="badge ${m.tipo}">${m.tipo === "entrada" ? "Entrada" : "Saída"}</span></td>
        <td>${m.tipo === "entrada" ? "+" : "−"}${m.quantidade}</td>
        <td class="l">${m.descricao}</td>
        <td><strong>${m.estoque_resultante}</strong></td>
      </tr>`
    )
    .join("");
}

function selecionarTipo(tipo) {
  tipoSelecionado = tipo;
  document.querySelectorAll("#tipo button").forEach((b) => {
    b.classList.toggle("ativo", b.dataset.tipo === tipo);
  });
}

async function lancar() {
  const feedback = el("#feedback");
  feedback.className = "feedback";
  feedback.textContent = "";

  const codigo = Number(el("#produto").value);
  const quantidade = Number(el("#quantidade").value);
  const descricao = el("#descricao").value;

  const r = await window.pywebview.api.movimentar(
    codigo,
    tipoSelecionado,
    quantidade,
    descricao
  );

  if (!r.ok) {
    feedback.className = "feedback erro";
    feedback.textContent = "⚠ " + r.erro;
    return;
  }

  const m = r.movimentacao;
  feedback.className = "feedback ok";
  feedback.innerHTML =
    `✓ Movimentação #${m.id} registrada (${m.produto_descricao}).<br>` +
    `Estoque final do produto: <span class="big">${r.estoque_final}</span> un`;

  renderProdutos(r.produtos, codigo);
  preencherSelect(r.produtos);
  el("#produto").value = String(codigo);
  renderHistorico(r.movimentacoes);
  el("#descricao").value = "";
  el("#quantidade").value = "1";
}

aguardarApi().then(() => {
  iniciar();
  el("#lancar").addEventListener("click", lancar);
  el("#recarregar").addEventListener("click", async () => {
    const estado = await window.pywebview.api.reiniciar();
    if (!estado.ok) return;
    renderProdutos(estado.produtos);
    preencherSelect(estado.produtos);
    renderHistorico(estado.movimentacoes);
    const fb = el("#feedback");
    fb.className = "feedback";
    fb.textContent = "";
  });
  document.querySelectorAll("#tipo button").forEach((b) => {
    b.addEventListener("click", () => selecionarTipo(b.dataset.tipo));
  });
});
