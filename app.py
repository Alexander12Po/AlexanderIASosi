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

    data = {
        "contents": [
            {
                "parts": [
                    {"text": mensaje}
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
