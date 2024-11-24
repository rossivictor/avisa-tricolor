from flask import Flask, request, Response, render_template
import bot
import json
from config import opcoes_setores

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jogos", methods=["GET"])
def jogos():
    jogos_disponiveis = bot.lista_jogos()

    print("\n\n\napp.py [jogos disponíveis]:\n")
    print(jogos_disponiveis)
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
            json.dumps({"erro": str(e)}, ensure_ascii=False),
            content_type="application/json; charset=utf-8",
            status=500
        )

@app.route("/bot", methods=["POST"])
def iniciar_bot():
    data = request.json
    jogo_link = data["link"]
    setor_id = data["setor_id"]

    return bot.pesquisa_ingresso(jogo_link, setor_id)

if __name__ == "__main__":
    app.run(debug=True)