document.addEventListener('DOMContentLoaded', async () => {
    const listaJogos = document.querySelector('.lista-jogos');

    try {
        const response = await fetch('/jogos');
        const jogos = await response.json();

        jogos.forEach((jogo) => {
            const li = document.createElement('li');
            const button = document.createElement('button');

            button.textContent = jogo.nome;
            button.addEventListener('click', () => exibirSetores(jogo));
            console.log({jogo})

            li.appendChild(button);
            listaJogos.appendChild(li);
        });
    } catch (error) {
        console.error(error);
    }
});

async function exibirSetores(jogo) {
    const listaJogos = document.querySelector('.lista-jogos');
    const titulo = document.querySelector('p');
    titulo.textContent = `Escolha um setor para o jogo: ${jogo.nome}`;

    try {
        const response = await fetch('/setores');
        const setores = await response.json();
        console.log("Setores: " + setores);

        listaJogos.innerHTML = "";
        setores.forEach((setor, id) => {
            const li = document.createElement('li');
            const button = document.createElement('button');

            button.textContent = setor;
            button.addEventListener('click', async () => {
                await selecionarSetor(id, jogo);
            });
            console.log({jogo});

            li.appendChild(button);
            listaJogos.appendChild(li);
        });
    } catch (error) {
        listaJogos.innerHTML = `<li>Erro ao carregar setores: ${error.message}`;
    }
}

async function selecionarSetor(setor_id, jogo) {
    const listaJogos = document.querySelector('.lista-jogos'); // Lista de setores
    const titulo = document.querySelector('p'); // Título da página

    // Atualizar a interface para indicar que a busca está em andamento
    titulo.textContent = `${jogo.nome}`;
    listaJogos.innerHTML = `
        <li>Buscando ingresso: ${jogo.nome}</li>
        <li>Setor escolhido: Carregando...</li>
        <li>⏳ Aguarde, estamos tentando encontrar o ingresso para você...</li>
    `;

    try {
        // Buscando os setores no back-end
        const setoresResponse = await fetch('/setores');
        const opcoesSetores = await setoresResponse.json();

        listaJogos.innerHTML = `
            <li>Buscando ingresso: ${jogo.nome}</li>
            <li>Setor escolhido: ${opcoesSetores[setor_id]}</li>
            <li>⏳ Aguarde, estamos tentando encontrar o ingresso para você...</li>
        `;

        // Disparar o bot no back-end
        const response = await fetch('/bot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                setor_id,
                link: jogo.link,
            }),
        });

        const data = await response.json();

        // Exibir o resultado
        if (data.mensagem === "Ingresso encontrado!") {
            listaJogos.innerHTML = `
                <li>🎉 ${data.mensagem}</li>
                <li><a href="${data.link}" target="_blank">Clique aqui para comprar seu ingresso!</a></li>
            `;
        } else {
            listaJogos.innerHTML = `<li>⚙️ ${data.mensagem}</li>`;
        }
    } catch (error) {
        listaJogos.innerHTML = `<li>❌ Erro ao buscar ingresso: ${error.message}</li>`;
    }
}