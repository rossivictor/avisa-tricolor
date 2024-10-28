import random
import time
import requests

destino_bot = input("Cole o endereço do site: \n")
flag = input("Que ingresso você quer? \n")

def bot(destino_bot, flag):
    intervalo = [30, 45, 18, 20]
    encontrado = False

    def disparo_alerta():
        print("Ingresso disponível agora:", time.strftime("%Y-%m-%d %H:%M:%S"))

    def query(destino_bot):
        def verificacao_status(conteudo_pagina):
            return flag in conteudo_pagina
        
        def request(destino_bot):
            response = requests.get(destino_bot)
            if response.status_code == 200:
                return response.text
            else:
                print("Erro:", response.status_code)
                return None

        conteudo_pagina = request(destino_bot)
        
        if conteudo_pagina:
            status_ingresso = verificacao_status(conteudo_pagina)
            return {"disponivel": status_ingresso}
        else:
            return {"disponivel": False}
        
    def pesquisa_ingresso():
        nonlocal encontrado
        tentativa = 0
        print("Aguardando tentativa. Fique frio, vai dar tudo certo. :)")

        while not encontrado:
            time.sleep(random.choice(intervalo))
            tentativa += 1 
            print(f"Tentativa #{tentativa}:", time.strftime("%Y-%m-%d %H:%M:%S"))
            resultado_query = query(destino_bot)
            if resultado_query["disponivel"]:
                encontrado = True
                disparo_alerta()
    
    pesquisa_ingresso()

bot(destino_bot,flag)


