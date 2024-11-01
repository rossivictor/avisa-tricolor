from bs4 import BeautifulSoup
import random
import time
import requests

def bot():
    intervalo = [30, 45, 18, 20]
    encontrado = False

    def lista_jogos():
        destino_bot = "https://www.spfcticket.net/"
        response = requests.get(destino_bot)
        html_parseado = BeautifulSoup(response.text, 'html.parser')
        todos_jogos = html_parseado.select('.card-jogo')

        jogos_disponiveis = []

        if todos_jogos:
            print("\n* Bilheteria aberta *\n")
            for index, jogo in enumerate(todos_jogos):
                botao_comprar = jogo.select_one('a.btn.btn-primary') 

                if botao_comprar and 'Comprar agora' in botao_comprar.text:
                    nome = jogo.select_one('.jogo-title').text.strip()
                    link = botao_comprar.get('href')
                    print(f"  [{index}] - {nome}")
                    jogos_disponiveis.append(link)            


            if jogos_disponiveis:
                escolha = int(input("\n Escolha o jogo: "))
                return jogos_disponiveis[escolha]
        
        else:
            print("Nenhum jogo disponível, tente novamente mais tarde.")
            print("Enquanto isso, assista o antológico Gol 100 do Rogério Ceni: https://www.youtube.com/watch?v=q0bzabZyWNk")
            return None

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

        conteudo_pagina = request(destino_bot)
        
        if conteudo_pagina:
            html_parseado = BeautifulSoup(conteudo_pagina, 'html.parser')
            link_pagina_compra = html_parseado.select('li a.btn.btn-primary')[0].get('href')
            print(link_pagina_compra)
        
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
    if jogo_escolhido:  # Verifica se um jogo foi escolhido
        pesquisa_ingresso(jogo_escolhido)

# debug()
bot()
