from bs4 import BeautifulSoup
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def lista_jogos():
    destino_bot = "https://www.spfcticket.net/"
    response = requests.get(destino_bot)
    html_parseado = BeautifulSoup(response.text, 'html.parser')
    todos_jogos = html_parseado.select('.card-jogo')

    jogos_disponiveis = []

    if todos_jogos:
        for index, jogo in enumerate(todos_jogos):
            botao_comprar = jogo.select_one('a.btn.btn-primary')
            if botao_comprar and 'Comprar agora' in botao_comprar.text:
                nome = jogo.select_one('.jogo-title').text.strip()
                link = botao_comprar.get('href')
                jogos_disponiveis.append((index, nome, link))
        return jogos_disponiveis
    return []

def escolha_setor(setores_disponiveis):
    print("\n🏟️ Setores disponíveis:")
    for idx, setor in setores_disponiveis.items():
        print(f"  [{idx}] - {setor}")

    setor_escolhido = int(input("\n * Escolha o setor 👉 "))
    return setores_disponiveis[setor_escolhido]

def pesquisa_ingresso(jogo_escolhido, setor_escolhido):
    intervalo = [30, 45, 18, 20]
    tentativa = 0
    encontrado = False

    def renderiza_pagina(link):
        params = webdriver.ChromeOptions()
        params.add_argument('--headless')
        navegador = webdriver.Chrome(options=params)
        navegador.get(link)

        try:
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameAndLot")))
        except Exception as e:
            print(f"\n ⚙️ Nenhum ingresso disponível: {e}")

        pagina_renderizada = BeautifulSoup(navegador.page_source, "html.parser")
        navegador.quit()
        return pagina_renderizada

    while not encontrado:
        if tentativa >= 1:
            print(f"⚙️ Tentativa #{tentativa}: {time.strftime('%H:%M:%S')}")

        html_parseado = renderiza_pagina(jogo_escolhido)

        setores_disponiveis = html_parseado.find_all('div', class_='cart-product-group-item')
        for setor in setores_disponiveis:
            if setor_escolhido in setor.text and 'Esgotado' not in setor.text:
                encontrado = True
                print("🚨 Ingresso disponível agora:", time.strftime("%H:%M:%S"))
                print("➡️ Link:", jogo_escolhido)
                print("\n🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇳🇱")
                return True

        tentativa += 1
        time.sleep(random.choice(intervalo))

    return False

def bot():
    
    jogos = lista_jogos()
    if not jogos:
        print("\n❌ Nenhum jogo disponível no momento.")
        return

    print("\nBilheteria aberta\n")
    for index, nome, _ in jogos:
        print(f"  [{index}] - {nome}")

    escolha = int(input("\n * Digite a opção e escolha o jogo 👉 "))
    jogo_escolhido = jogos[escolha][2]

    dicionario_setores = {
        0: "Arquibancada Norte Oero - Inteira",
        1: "Arquibancada Leste Lacta - Inteira",
        2: "Arquibancada Sul Diamante Negro - Meia",
        3: "Arquibancada Sul Diamante Negro - Inteira",
        4: "Arquibancada Visitante Ouro Branco - Meia",
        5: "Arquibancada Visitante Ouro Branco - Inteira",
        6: "Cadeira Superior Norte Oero - Inteira",
        7: "Cadeira Superior Sul Diamante Negro - Meia",
        8: "Cadeira Especial Oeste Ouro Branco - Especial Inteira",
        9: "Cadeira Térrea Oeste Ouro Branco - Meia",
        10: "Camarote dos Ídolos - Único",
    }

    setor_escolhido = escolha_setor(dicionario_setores)

    print("\n ✅ Pronto! Deixe a janela aberta e aguarde enquanto procuramos o ingresso.")

    encontrado = pesquisa_ingresso(jogo_escolhido, setor_escolhido)

    if encontrado:
        print("\n🎉 Ingresso encontrado com sucesso! Aproveite o jogo!")
    else:
        print("\n❌ Não foi possível encontrar o ingresso. Tente novamente mais tarde.")

# Só roda o bot no CLI, se executado diretamente
if __name__ == "__main__":
    bot()

# !TO-DO: Rodar a página escolhida para fazer o scrap e pegar o link do botão de compra certo
