from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Validar que la API key esté configurada
        if not API_KEY:
            return jsonify({"respuesta": "API key no configurada"}), 500
        
        # Obtener y validar el mensaje
        mensaje = request.json.get("mensaje")
        if not mensaje or not mensaje.strip():
            return jsonify({"respuesta": "El mensaje no puede estar vacío"}), 400
        
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
        
        r = requests.post(url, json=data, timeout=10)
        
        if r.status_code == 200:
            try:
                respuesta = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"respuesta": respuesta})
            except (KeyError, IndexError):
                return jsonify({"respuesta": "Error al procesar la respuesta"}), 500
        
        return jsonify({"respuesta": "Error al conectar con Gemini"}), r.status_code
        
    except requests.exceptions.RequestException as e:
        return jsonify({"respuesta": "Error de conexión"}), 500
    except Exception as e:
        return jsonify({"respuesta": "Error interno del servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
