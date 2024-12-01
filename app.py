from flask import Flask, request, Response, render_template
import bot
import json
import time
import random
from config import opcoes_setores

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jogos", methods=["GET"])
def jogos():
    jogos_disponiveis = bot.lista_jogos()
    
    return Response(json.dumps(jogos_disponiveis, ensure_ascii=False), content_type="application/json")

@app.route("/setores", methods=["GET"])
def setores():
    try:
        return Response(
            json.dumps(opcoes_setores, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            json.dumps({"Erro": str(e)}),
            content_type="application/json; charset=utf-8"
        )

@app.route("/bot", methods=["GET"])
def bot_disparador():
    jogo_link = request.args.get('jogo_link')
    setor_id = request.args.get('setor_id')

    if not jogo_link or not setor_id:
        return Response("data: Parâmetros inválidos\n\n", content_type="text/event-stream")

    def ciclo_eventos():
        tentativa = 0
        while True:
            tentativa += 1
            resultado = bot.query(jogo_link, int(setor_id))

            if resultado["disponivel"]:
                yield f"data: {{\"status\": \"disponivel\", \"link\": \"{resultado['link']}\", \"tentativa\": {tentativa}}}\n\n"
                break
            else:
                yield f"data: {{\"status\": \"tentando\", \"message\": \"Ainda tentando...\", \"tentativa\": {tentativa}}}\n\n"
                time.sleep(random.choice([30, 45, 18, 20]))

    return Response(ciclo_eventos(), content_type="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)