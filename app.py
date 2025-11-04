from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load secrets
N8N_URL = os.getenv("N8N_WEBHOOK_URL")
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get("text")
        mode = data.get("mode")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY   # ✅ Secret header stays server-side
        }

        payload = {"text_to_analyze": text, "mode": mode}
        response = requests.post(N8N_URL, headers=headers, json=payload)
        response_data = response.json()

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
