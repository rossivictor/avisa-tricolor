from bs4 import BeautifulSoup
import random
import time
import requests

def bot():
    intervalo = [30, 45, 18, 20]
    encontrado = False

    def lista_jogos():
        destino_bot = "https://www.spfcticket.net/proximos-jogos/"
        response = requests.get(destino_bot)
        html_parseado = BeautifulSoup(response.text, 'html.parser')
        todos_jogos = html_parseado.find_all(class_='card-jogo')
        
        if todos_jogos:
            print("Jogos disponíveis: ")
            
            index = 0
            for jogo in todos_jogos:
                nome = html_parseado.select('.card-jogo a img')[index].get('title')
                print(f"[{index}] - {nome}")
                index += index

            escolha = int(input("Escolha o jogo: "))

            return html_parseado.select('.card-jogo a')[escolha].get('href')

        return print("Nenhum jogo disponível, tente novamente mais tarde.", "Enquanto isso, assista o antológico Gol 100 do Rogério Ceni: https://www.youtube.com/watch?v=q0bzabZyWNk")

    def disparo_alerta():
        print("Ingresso disponível agora:", time.strftime("%Y-%m-%d %H:%M:%S"))

    def query(destino_bot):
        def request(destino_bot):
            response = requests.get(destino_bot)
            if response.status_code == 200:
                return response.text
            else:
                print("Erro:", response.status_code)
                return None
        
        # flag = input("Que ingresso você quer? \n")
        conteudo_pagina = request(destino_bot)
        
        if conteudo_pagina:
            html_parseado = BeautifulSoup(conteudo_pagina, 'html.parser')
            todos_jogos = html_parseado.find_all(class_='card-jogo')
            print(todos_jogos)
            for jogo in todos_jogos:
                print(jogo.get('href'))
            return {"disponivel": True}
        
        else:
            return {"disponivel": False}
        
    def pesquisa_ingresso(destino_bot):
        tentativa = 0
        nonlocal encontrado
        while not encontrado:
            tentativa += 1 
            print(f"Tentativa #{tentativa}:", time.strftime("%Y-%m-%d %H:%M:%S"))
            resultado_query = query(destino_bot)
            if resultado_query["disponivel"]:
                encontrado = True
                disparo_alerta()
            time.sleep(random.choice(intervalo))
    
    jogo_escolhido = lista_jogos()
    pesquisa_ingresso(jogo_escolhido)

# debug()
bot()
