from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "AQ.Ab8RN6IlHAMXvQl5Hwhcg_BqXaS07S-l9a-FDCvB8tn-pTlIeA"

MODEL = "gemini-2.5-flash"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.json.get("mensaje")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

    prompt = f"""
Eres SOSI, un asistente de inteligencia artificial experto en programación.

Reglas:
- Responde siempre en español.
- Cuando generes código, usa siempre bloques Markdown.
- Especifica el lenguaje del código (html, css, javascript, python, etc.).
- Nunca envíes código como texto plano.
- Explica brevemente qué hace el código antes de mostrarlo.
- Si el usuario pide un archivo completo, entrégalo completo.

Mensaje del usuario:
{mensaje}
"""

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    r = requests.post(url, json=data)

    if r.status_code == 200:
        respuesta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"respuesta": respuesta})

    return jsonify({"respuesta": "Error al conectar con Gemini."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
