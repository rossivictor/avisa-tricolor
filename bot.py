from bs4 import BeautifulSoup
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import opcoes_setores, dicionario_setores

intervalo = [30, 45, 18, 20]

def request(destino_bot):    
    response = requests.get(destino_bot)
    if response.status_code == 200:
        return response.text
    else:
        print("Erro:", response.status_code)
    return None

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
                jogos_disponiveis.append({"nome": nome, "link": link})
    
    print("\n\n\nbot.py [jogos disponíveis]:\n")
    print(jogos_disponiveis)
    return jogos_disponiveis

def verifica_ingresso(setor_escolhido, link):
    print(f"Setor escolhido:", setor_escolhido)
    print(f"Link:", link)
    def renderiza_pagina(link):
        params = webdriver.ChromeOptions()
        params.add_argument('--headless') 
        navegador = webdriver.Chrome(options=params)
        navegador.get(link)
        
        try:
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameAndLot")))
        except:
            print("\n ⚙️ Nenhum ingresso disponível, tentando novamente... \n")

        pagina_renderizada = BeautifulSoup(navegador.page_source, "html.parser")
        navegador.quit()
        return pagina_renderizada
    
    html_parseado = renderiza_pagina(link)
    
    setores_disponiveis = html_parseado.find_all('div', class_='cart-product-group-item')

    for setor in setores_disponiveis:
        if dicionario_setores[setor_escolhido] in setor.text and 'Esgotado' not in setor.text:
            return True

    return False

def disparo_alerta(link):
    print("🚨 Ingresso disponível agora:", time.strftime("%H:%M:%S"))
    print("➡️ Link:", link)
    return print("\n🎉 Bom jogo, Tricolor! Vamos São Paulo! 🇳🇱")

def query(destino_bot, setor_escolhido):
    def parseador_link(link):
        response = request(link)
        html_parseado_jogos = BeautifulSoup(response, 'html.parser')
        link_pagina_compra = html_parseado_jogos.select('li a.btn.btn-primary')[0].get('href')
        return link_pagina_compra
    
    link_parseado = parseador_link(destino_bot)

    if link_parseado:
        if 'cart' not in link_parseado:
            link_parseado = parseador_link(link_parseado)
        status = verifica_ingresso(setor_escolhido, link_parseado)
        return {
            "disponivel": status,
            "link": link_parseado 
        }
    
    else:
        return {"disponivel": False}

def pesquisa_ingresso(jogo_escolhido, setor_escolhido):
    tentativa = 0
    encontrado = False
    if tentativa == 0: 
        print('\n ✅ Pronto! Deixe a janela aberta, aguarde e deixe as máquinas trabalharem 🖐🏽 \n')
    while not encontrado:
        if tentativa >= 1:
            print(f"⚙️ Tentativa #{tentativa}:", time.strftime("%H:%M:%S"))
        
        resultado_query = query(jogo_escolhido, setor_escolhido)
        
        if resultado_query["disponivel"]:
            encontrado = True
            return disparo_alerta(resultado_query["link"])
        else:
            tentativa += 1
            time.sleep(random.choice(intervalo)) # respira um pouco.

# CLI original
if __name__ == "__main__":
    jogos = lista_jogos()
    if not jogos:
        print("Nenhum jogo disponível.")
        exit()

    print("Jogos disponíveis:")
    for i, jogo in enumerate(jogos):
        print(f"[{i}] - {jogo['nome']}")

    escolha_jogo = int(input("Escolha um jogo: "))
    jogo_escolhido = jogos[escolha_jogo]

    print("\nSetores disponíveis:")
    for i, setor in enumerate(opcoes_setores):
        print(f"[{i}] - {setor}")

    escolha_setor = int(input("Escolha um setor: "))
    resultado = verifica_ingresso(jogo_escolhido["link"], escolha_setor)

    if resultado["disponivel"]:
        print("Ingresso disponível! Link:", resultado["link"])
    else:
        print("Ainda não há ingressos disponíveis.")