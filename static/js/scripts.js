document.addEventListener("DOMContentLoaded", async () => {
  const appCore = document.querySelector("#core");

  try {
    const response = await fetch("/jogos");
    const jogos = await response.json();

    jogos.forEach((jogo) => {
      const button = document.createElement("button");
      const jogoDados = parseJogo(jogo.nome);
      console.log(jogoDados);

      button.innerHTML = `<strong>${jogoDados.timeCasa}</strong> x <strong>${jogoDados.timeVisitante}</strong><br /><span>${jogoDados.campeonato}`;
      button.addEventListener("click", () => exibirSetores(jogo));

      appCore.appendChild(button);
    });
  } catch (error) {
    console.error(error);
  }
});

function parseJogo(nomeJogo) {
  const partes = nomeJogo.replace(" – ", ",").replace(" x ", ",").split(",");
  const resultado = partes.map((parte) => parte.trim());
  const jogoElementos = {
    timeCasa: resultado[0],
    timeVisitante: resultado[1],
    campeonato: resultado[2],
  };

  return jogoElementos;
}

async function exibirSetores(jogo) {
  const appCore = document.querySelector("#core");
  const passo = document.querySelector(".card h3");
  const legenda = document.querySelector(".card p");
  const jogoDados = parseJogo(jogo.nome);
  passo.innerHTML = "2º passo:";
  legenda.innerHTML = `Escolha um setor para ver o jogo contra o <strong>${jogoDados.timeVisitante}</strong>`;
  console.log(
    jogoDados.timeCasa,
    jogoDados.timeVisitante,
    jogoDados.campeonato
  );

  try {
    const response = await fetch("/setores");
    const setores = await response.json();

    appCore.innerHTML = "";
    const select = document.createElement("select");
    appCore.appendChild(select);

    setores.forEach((setor, id) => {
      const option = document.createElement("option");
      option.textContent = setor;
      option.value = id;
      select.appendChild(option);
    });

    select.addEventListener("change", async () => {
      const opcaoSelecionada = select.options[select.selectedIndex];
      const setorId = opcaoSelecionada.value;
      const setorNome = opcaoSelecionada.textContent;

      await selecionarSetor(setorId, setorNome, jogo);
    });
  } catch (error) {
    appCore.innerHTML = `<li>Erro ao carregar setores: ${error.message}`;
  }
}

async function selecionarSetor(setor_id, setor_nome, jogo) {
  const appCore = document.querySelector("#core");
  const titulo = document.querySelector("p");
  const mensagens = document.querySelector("#mensagens");
  const setorId = encodeURIComponent(setor_id);
  const setorNome = encodeURIComponent(setor_nome);
  const jogoNome = encodeURIComponent(jogo.nome);
  const jogoLink = encodeURIComponent(jogo.link);
  const botEndpoint = `/bot?jogo_link=${jogoLink}&setor_id=${setorId}`;

  appCore.innerHTML = "";
  mensagens.innerHTML = `<p>✅ Pronto! Deixe a janela aberta e aguarde enquanto as máquinas trabalham para você! 🖐🏽</p>`;

  const eventSource = new EventSource(botEndpoint);

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.status === "disponivel") {
      alert(`AVISA TRICOLOR: 🚨 Ingresso disponível! Corre pra comprar!`);
      mensagens.innerHTML = `
                <p>🚨 Ingresso disponível agora: ${new Date().toLocaleTimeString()}</p>
                <p>➡️ Link: <a href="${data.link}" target="_blank">${
        data.link
      }</a></p>
                <p>🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇪🇬</p>
            `;
      eventSource.close();
    } else if (data.status === "tentando") {
      const tentativa = data.tentativa || 1;
      const logP = document.querySelector("#logContainer p");
      logP.innerHTML =
        "⚙️ Ainda não conseguimos, mas vamos continuar tentando!";
      const logUl = document.querySelector("#logContainer ul");
      const novoLog = document.createElement("li");
      novoLog.innerHTML = `Tentativa ${tentativa}: ${new Date().toLocaleTimeString()}`;
      logUl.prepend(novoLog);
    }
  };

  eventSource.onerror = (error) => {
    alert(
      "AVISA TRICOLOR: 😰 Houve um erro no servidor. Tente novamente!",
      error
    );
    mensagens.innerHTML += `<p>❌ Ocorreu um erro ao tentar se conectar ao servidor. Por favor, tente atualizar a página e tentar novamente.</p>`;
    eventSource.close();
  };
}
