document.addEventListener("DOMContentLoaded", async () => {
  const listaJogos = document.querySelector(".lista-jogos");

  try {
    const response = await fetch("/jogos");
    const jogos = await response.json();

    jogos.forEach((jogo) => {
      const li = document.createElement("li");
      const button = document.createElement("button");

      button.textContent = jogo.nome;
      button.addEventListener("click", () => exibirSetores(jogo));

      li.appendChild(button);
      listaJogos.appendChild(li);
    });
  } catch (error) {
    console.error(error);
  }
});

async function exibirSetores(jogo) {
  const listaJogos = document.querySelector(".lista-jogos");
  const titulo = document.querySelector("p");
  titulo.textContent = `Escolha um setor para o jogo: ${jogo.nome}`;

  try {
    const response = await fetch("/setores");
    const setores = await response.json();

    listaJogos.innerHTML = "";
    setores.forEach((setor, id) => {
      const li = document.createElement("li");
      const button = document.createElement("button");

      button.textContent = setor;
      button.addEventListener("click", async () => {
        await selecionarSetor(id, setor, jogo);
      });

      li.appendChild(button);
      listaJogos.appendChild(li);
    });
  } catch (error) {
    listaJogos.innerHTML = `<li>Erro ao carregar setores: ${error.message}`;
  }
}

async function selecionarSetor(setor_id, setor_nome, jogo) {
  const listaJogos = document.querySelector(".lista-jogos");
  const titulo = document.querySelector("p");
  const mensagens = document.querySelector("#mensagens");
  const setorId = encodeURIComponent(setor_id);
  const setorNome = encodeURIComponent(setor_nome);
  const jogoNome = encodeURIComponent(jogo.nome);
  const jogoLink = encodeURIComponent(jogo.link);
  const botEndpoint = `/bot?jogo_link=${jogoLink}&setor_id=${setorId}`;

  listaJogos.innerHTML = "";
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
