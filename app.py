from flask import Flask, render_template, request, jsonify
import requests, base64

app = Flask(__name__)

API_KEYS=[
    "AQ.Ab8RN6IlHAMXvQl5Hwhcg_BqXaS07S-l9a-FDCvB8tn-pTlIeA",
    "AQ.Ab8RN6J_ga5dGTx1PJXMlOEEcj6KDFe_IqXaJc-vi_mF1iYOxQ",
    "AQ.Ab8RN6JkYDB_saQ7RI0hPzYfNI37eXOuxXAZW7HDOViqX7Nb5A"
]

MODEL="gemini-2.5-flash"

PROMPT_BASE="""Eres SOSI, un asistente experto en programación.
- Responde siempre en español.
- Usa bloques Markdown para el código.
- Explica brevemente el código antes de mostrarlo.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    mensaje=request.form.get("mensaje","")
    imagen=request.files.get("imagen")

    parts=[{"text":PROMPT_BASE+"\n\nMensaje del usuario:\n"+mensaje}]

    if imagen:
        parts.append({
            "inline_data":{
                "mime_type": imagen.mimetype or "image/jpeg",
                "data": base64.b64encode(imagen.read()).decode("utf-8")
            }
        })

    payload={"contents":[{"parts":parts}]}

    for key in API_KEYS:
        url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
        try:
            r=requests.post(url,json=payload,timeout=60)
            if r.status_code==200:
                j=r.json()
                return jsonify({"respuesta":j["candidates"][0]["content"]["parts"][0]["text"]})
            if r.status_code==429:
                print("Cuota agotada, probando siguiente API Key...")
                continue
            print(r.text)
        except Exception as e:
            print(e)
            continue

    return jsonify({"respuesta":"Todas las API Keys fallaron o agotaron su cuota."}),500

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    
