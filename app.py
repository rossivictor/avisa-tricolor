from flask import Flask, render_template, Response, request
import json
import bot

app = Flask(__name__)

opcoes_setores = [
    "Arquibancada Norte Oreo - Inteira",
    "Arquibancada Leste Lacta - Meia",
    "Arquibancada Leste Lacta - Inteira",
    "Arquibancada Sul Diamante Negro - Meia",
    "Arquibancada Sul Diamante Negro - Inteira",
    "Arquibancada Visitante Ouro Branco - Meia",
    "Arquibancada Visitante Ouro Branco - Inteira",
    "Cadeira Superior Norte Oreo - Inteira",
    "Cadeira Superior Sul Diamante Negro - Meia",
    "Cadeira Superior Sul Diamante Negro - Inteira",
    "Cadeira Especial Oeste Ouro Branco - Especial Meia",
    "Cadeira Especial Oeste Ouro Branco - Especial Inteira",
    "Cadeira Térrea Oeste Ouro Branco - Meia",
    "Cadeira Térrea Oeste Ouro Branco - Inteira",
    "Camarote Corporativo SPFC - Único",
    "Camarote dos Ídolos - Único"
]

dicionario_setores = [
    "ARQUIBANCADA NORTE OREO - Inteira",
    "ARQUIBANCADA LESTE LACTA - Meia",
    "ARQUIBANCADA LESTE LACTA - Inteira",
    "ARQUIBANCADA SUL DIAMANTE NEGRO - Meia",
    "ARQUIBANCADA SUL DIAMANTE NEGRO - Inteira",
    "ARQUIBANCADA VISITANTE OURO BRANCO - Meia",
    "ARQUIBANCADA VISITANTE OURO BRANCO - Inteira",
    "CADEIRA SUPERIOR NORTE OREO - Inteira",
    "CAD. SUP. SUL DIAMANTE NEGRO - Meia",
    "CAD. SUP. SUL DIAMANTE NEGRO - Inteira",
    "CAD. ESP. OESTE OURO BRANCO - Especial Meia",
    "CAD. ESP. OESTE OURO BRANCO - Especial Inteira",
    "CAD. TÉRREA OESTE OURO BRANCO - Meia",
    "CAD. TÉRREA OESTE OURO BRANCO - Inteira",
    "CAMAROTE CORPORATIVO SPFC - Único",
    "CAMAROTE DOS ÍDOLOS - Único"
]

@app.route("/")
def avisa_tricolor():
    return render_template("index.html")


@app.route("/jogos", methods=["GET"])
def lista_jogos():
    try:
        jogos_disponiveis = bot.lista_jogos()

        if not jogos_disponiveis:
            return Response(
                json.dumps({"erro": "Nenhum jogo disponível"},
                ensure_ascii=False),
                content_type="application/json; charset=utf-8",
                status=404
            )
        
        return Response(
            json.dumps(
                [{"id": index, "nome": nome, "link": link} for index, nome, link in jogos_disponiveis],ensure_ascii=False
                ),
            content_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            json.dumps({"erro": str(e)}, ensure_ascii=False), 
            content_type="application/json; charset=utf-8", 
            status=500
        )
    
@app.route("/setores", methods=["GET"])
def lista_setores():
    return Response(
        json.dumps(opcoes_setores, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )
    
@app.route("/bot", methods=["POST"])
def inicia_bot():
    try:
        data = request.json
        setor_id = data.get("setor_id")
        jogo_nome = data.get("jogo_nome")

        if setor_id is None or setor_id < 0 or setor_id >= len(dicionario_setores):
            return Response(
                json.dumps({"erro": "Setor inválido"}, ensure_ascii=False),
                content_type="application/json; charset=utf-8",
                status=400
            )
        
        setor_escolhido = dicionario_setores[setor_id]

        print(f"Iniciando o bot para o jogo: {jogo_nome} e setor: {setor_escolhido}")
        # bot.pesquisa_ingresso(jogo_nome, setor_escolhido)

        return Response(
            json.dumps({"mensagem": f"Bot iniciado para o jogo: {jogo_nome} e setor: {setor_escolhido}"},
                       ensure_ascii=False),
                    content_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            json.dumps({"erro": str(e)}, ensure_ascii=False),
            content_type="application/json; charset=utf-8",
            status=500
        )

if __name__ == "__main__":
    app.run(debug=True)