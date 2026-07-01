from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Coloca aquí todas tus API Keys
API_KEYS = [
    "AQ.Ab8RN6IlHAMXvQl5Hwhcg_BqXaS07S-l9a-FDCvB8tn-pTlIeA",
    "AQ.Ab8RN6J_ga5dGTx1PJXMlOEEcj6KDFe_IqXaJc-vi_mF1iYOxQ",
    "AQ.Ab8RN6JkYDB_saQ7RI0hPzYfNI37eXOuxXAZW7HDOViqX7Nb5A"
]

MODEL = "gemini-2.5-flash"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    mensaje = request.json.get("mensaje")

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

    # Probar cada API Key hasta encontrar una que funcione
    for API_KEY in API_KEYS:

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

        try:
            r = requests.post(url, json=data, timeout=30)

            if r.status_code == 200:
                respuesta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"respuesta": respuesta})

            # Si la cuota está agotada, probar la siguiente Key
            if r.status_code == 429:
                print(f"API agotada: {API_KEY[:12]}...")
                continue

        except Exception:
            continue

    return jsonify({
        "respuesta": "Todas las API Keys alcanzaron su límite de uso."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
