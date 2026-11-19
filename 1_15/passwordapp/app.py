import hashlib
import secrets
import string
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecTools - Salasana & SHA-256</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #121212; color: #e0e0e0; max-width: 600px; margin: 40px auto; padding: 20px; }
        .card { background: #1e1e1e; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }
        h2 { margin-top: 0; color: #4caf50; }
        input, button { padding: 10px; border-radius: 4px; border: 1px solid #444; background: #2c2c2c; color: #fff; font-size: 14px; }
        input[type="text"] { width: 100%; box-sizing: border-box; margin-bottom: 10px; }
        input[type="number"] { width: 70px; margin-right: 10px; }
        button { background: #4caf50; border: none; cursor: pointer; font-weight: bold; }
        button:hover { background: #45a049; }
        .result { margin-top: 15px; padding: 10px; background: #000; border-radius: 4px; font-family: monospace; word-break: break-all; color: #00e676; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Salasanageneraattori</h2>
        <form method="POST">
            <label for="length">Pituus (8–64):</label>
            <input type="number" id="length" name="length" min="8" max="64" value="{{ length }}">
            <button type="submit" name="action" value="generate">Generoi salasana</button>
        </form>
        {% if password %}
            <div class="result">{{ password }}</div>
        {% endif %}
    </div>

    <div class="card">
        <h2>SHA-256 Tiiviste (Hash)</h2>
        <form method="POST">
            <input type="text" name="text" placeholder="Kirjoita teksti tähän..." value="{{ text }}" required>
            <button type="submit" name="action" value="hash">Laske SHA-256</button>
        </form>
        {% if hashed %}
            <div class="result">{{ hashed }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

def generate_secure_password(length: int) -> str:
    length = max(8, min(length, 64))
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    hashed = None
    length = 16
    text = ""

    if request.method == "POST":
        action = request.form.get("action")
        if action == "generate":
            try:
                length = int(request.form.get("length", 16))
            except ValueError:
                length = 16
            password = generate_secure_password(length)
        elif action == "hash":
            text = request.form.get("text", "")
            if text:
                hashed = compute_sha256(text)

    return render_template_string(
        HTML_TEMPLATE, password=password, hashed=hashed, length=length, text=text
    )

# API-rajapinnat
@app.route("/api/password", methods=["GET"])
def api_password():
    length = request.args.get("length", default=16, type=int)
    return jsonify({"password": generate_secure_password(length), "length": max(8, min(length, 64))})

@app.route("/api/hash", methods=["POST"])
def api_hash():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "Missing 'text' field in JSON body"}), 400
    return jsonify({"text": text, "sha256": compute_sha256(text)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
