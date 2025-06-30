from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

candidate_labels = [
    "Informative",
    "Promotional",
    "Emotional",
    "Opinion",
    "Personal Experience",
    "Academic",
    "News",
    "Question"
]

nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    text = data.get("text", "")
    res = nlp(text, candidate_labels)
    label = res["labels"][0]
    scores = dict(zip(res["labels"], res["scores"]))
    return jsonify({"label": label, "scores": scores})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
