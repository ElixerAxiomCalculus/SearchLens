from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/typeform/distilbert-base-uncased-mnli"
HF_TOKEN = os.getenv("HF_TOKEN")

CANDIDATE_LABELS = [
    "Informative",
    "Promotional",
    "Emotional",
    "Opinion",
    "Personal Experience",
    "Academic",
    "News",
    "Question"
]

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    text = data.get("text", "")
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": CANDIDATE_LABELS}
    }
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    res = response.json()
    label = res["labels"][0]
    scores = dict(zip(res["labels"], res["scores"]))
    return jsonify({"label": label, "scores": scores})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
