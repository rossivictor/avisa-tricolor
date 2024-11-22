document.addEventListener('DOMContentLoaded', async () => {
    const listaJogos = document.querySelector('.lista-jogos');
    const titulo = document.querySelector('p');

    try {
        const response = await fetch('/jogos');
        const jogos = await response.json();

        if (jogos.erro) {
            listaJogos.innerHTML = `<li>${jogos.erro}</li>`;
            return;
        }

        listaJogos.innerHTML = "";
        jogos.forEach((jogo) => {
            const li = document.createElement('li');
            const link = document.createElement('a');

            link.href = `#`;
            link.textContent = jogo.nome;
            link.addEventListener('click', async () => {
                await exibirSetores(jogo);
            });

            li.appendChild(link);
            listaJogos.appendChild(li);
        });
    } catch (error) {
        listaJogos.innerHTML = `<li>Erro ao carregar jogos: ${error.message}</li>`;
    }
});

async function exibirSetores(jogo) {
    const listaJogos = document.querySelector('.lista-jogos');
    const titulo = document.querySelector('p');
    titulo.textContent = `Escolha um setor para o jogo: ${jogo.nome}`;

    try {
        const response = await fetch('/setores');
        const setores = await response.json();

        listaJogos.innerHTML = "";
        setores.forEach((setor, id) => {
            const li = document.createElement('li');
            const button = document.createElement('button');

            button.textContent = setor;
            button.addEventListener('click', async () => {
                await selecionarSetor(id, jogo);
            });

            li.appendChild(button);
            listaJogos.appendChild(li);
        });
    } catch (error) {
        listaJogos.innerHTML = `<li>Erro ao carregar setores: ${error.message}`;
    }
}

async function selecionarSetor(setor_id, jogo) {
    try {
        const response = await fetch('/bot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ setor_id, jogo_nome: jogo.nome })
        });

        const data = await response.json();

        if (data.erro) {
            alert(`Erro: ${data.erro}`);
            return;
        }

        alert(data.mensagem);
    } catch (error) {
        alert(`Erro ao iniciar o bot: ${error.message}`);
    }
}