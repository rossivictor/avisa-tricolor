# avisa-tricolor

### Bot criado com o objetivo de avisar o torcedor quando o ingresso desejado está disponível para compra no site do SPFC

## Roadmap
* URL dinâmica entregando sempre próximo jogo ou lista de jogos
* Implementação de menu seletor com todos os setores disponíveis
* Deploy servidor stage / controlado
* botar lista de telefones avisados
* * link wa-me com telefones a avisar ou api whatsapp disparando

## Instrucoes

Esse bot executa dentro de um ambiente Python (3.x.x >). Caso nao tenha o ambiente configurado na sua maquina, siga antes as instrucoes de instalacao no site oficial do Python

E necessario que voce tenha instalado o *Google Chrome*. O bot utiliza o motor do Chrome para verificar informacoes necessarias. Provavelmente funciona com outros navegadores, mas precisa adaptar o driver para cada implementacao, usando o Chrome por ser o navegador mais popular e pelo Chromium em modo teste funcionar bem. Fique a vontade para alterar no codigo de acordo com a sua necessidade. Pull requests sao bem vindos.

Ja com o ambiente configurado:

* Instale via pip as dependencias rodando o seguinte comando:

### Usando `python3`
`pip3 install beautifulsoup4 requests selenium`

### Rodando o projeto

* Rode o comando `python3 bot.py`
* Siga as instrucoes da janela que ira abrir

