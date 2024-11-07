# avisa-tricolor

### Bot criado com o objetivo de avisar o torcedor quando o ingresso desejado está disponível para compra no site do SPFC

## Roadmap
* URL dinâmica entregando sempre próximo jogo ou lista de jogos ✅
* Implementação de menu seletor com todos os setores disponíveis ✅
* Implementação de função de notificação quando o ingresso estiver disponível
* Deploy servidor stage / controlado

## Instruções

Esse bot executa dentro de um ambiente Python (3.x.x >). Caso não tenha o ambiente configurado na sua maquina, siga antes as instruções de instalação no site oficial do Python

E necessario que você tenha instalado o *Google Chrome*. O bot utiliza o motor do Chrome para verificar informações necessárias. Provavelmente funciona com outros navegadores, mas precisa adaptar o driver para cada implementação, usando o Chrome por ser o navegador mais popular e pelo Chromium em modo teste funcionar bem. Fique à vontade para alterar no codigo de acordo com a sua necessidade. Pull requests são bem vindos.

Já com o ambiente configurado:

* Instale via pip as dependências rodando o seguinte comando:

### Usando `python3`
`pip3 install beautifulsoup4 requests selenium`

### Rodando o projeto

* Rode o comando `python3 bot.py`
* Siga as instruções da janela que irá abrir

