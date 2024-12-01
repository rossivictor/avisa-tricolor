from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import dicionario_setores

# Varre o site oficial e retorna um objeto com os jogos com vendas abertas.
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
                jogos_disponiveis.append({"index": index, "nome": nome, "link": link})

    return jogos_disponiveis

# Renderiza a página de compra e verifica se o setor escolhido está disponível.
def verifica_ingresso(setor_escolhido, link):
    def renderiza_pagina(link):
        params = webdriver.ChromeOptions()
        params.add_argument('--headless') 
        navegador = webdriver.Chrome(options=params)
        navegador.get(link)
        
        try:
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nameAndLot")))
        except:
            return {"⚙️ Nenhum ingresso disponível, tentando novamente..."}

        pagina_renderizada = BeautifulSoup(navegador.page_source, "html.parser")
        print("Página renderizada: ", pagina_renderizada)
        navegador.quit()
        return pagina_renderizada
    
    html_parseado = renderiza_pagina(link)
    print("HTML parseado: ", html_parseado)
    
    setores_disponiveis = html_parseado.find_all('div', class_='cart-product-group-item')
    print("Setores disponíveis: ", setores_disponiveis)

    for setor in setores_disponiveis:
        if dicionario_setores[setor_escolhido] in setor.text and 'Esgotado' not in setor.text:
            return True

    return False

# Verifica se o link está disponível e retorna o status.
def request(destino_bot):    
    response = requests.get(destino_bot)
    if response.status_code == 200:
        return response.text
    else:
        print("Erro:", response.status_code)
    return None

# Descobre o link da página de compra e roda `verifica_ingresso()`.
def query(jogo_link, setor_escolhido):
    def parseador_link(link):
        response = request(link)
        html_parseado_jogos = BeautifulSoup(response, 'html.parser')
        link_pagina_compra = html_parseado_jogos.select('li a.btn.btn-primary')[0].get('href')
        return link_pagina_compra
    
    compra_link = parseador_link(jogo_link)

    if compra_link:
        if 'cart' not in compra_link:
            compra_link = parseador_link(compra_link)
        status = verifica_ingresso(setor_escolhido, compra_link)

        return {
            "disponivel": status,
            "link": compra_link
        }
    
    else:
        return {"disponivel": False}
    