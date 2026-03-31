from flask import Flask, render_template, request, jsonify
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ai", methods=["POST"])
def ai_endpoint():
    data = request.json
    ai_type = data.get("type")
    text = data.get("text", "")
    character = data.get("character", "Luna")

    if ai_type == "correct":
        prompt = f"""Sen bir çocuk okuma koçusun. Bir kız çocuğu şu cümleyi okudu: "{text}". 
Nazik, sevgi dolu ve motive edici bir şekilde:
1. Doğru okunan kelimeleri tebrik et ✅
2. Düzeltilmesi gereken varsa şefkatle düzelt 💛
3. Ödüllendirici bir mesaj ver 🌟
Kısa tut, max 3 cümle. Türkçe yaz."""
    elif ai_type == "continue":
        prompt = f"""Sen {character} adlı bir masalın karakterisin. 
Bir çocuk sana şunu söyledi: "{text}"
Sihirli, sıcak ve sevgi dolu cevap ver. Max 2 cümle. Türkçe. Emoji kullan."""
    else:
        prompt = f"""Bir kız çocuğu için "{text}" konusunda 2 cümlelik sihirli mini hikaye yaz. Türkçe, sevimli. Emoji ekle."""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"reply": message.content[0].text})
    except Exception as e:
        return jsonify({"reply": "Sihir biraz kayboldu, tekrar dene! 🌙"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
