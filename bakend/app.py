from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

model_names = [
    "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    "facebook/bart-large-mnli",
    "typeform/distilbert-base-uncased-mnli"
]
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

pipelines = [pipeline("zero-shot-classification", model=name) for name in model_names]

def vote_label(results):
    votes = {}
    for res in results:
        label = res["labels"][0]
        votes[label] = votes.get(label, 0) + 1
    return max(votes, key=votes.get)

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    text = data.get("text", "")
    all_results = []
    for nlp in pipelines:
        res = nlp(text, candidate_labels)
        all_results.append(res)
    label = vote_label(all_results)
    scores = {i: [r["scores"][r["labels"].index(i)] if i in r["labels"] else 0 for r in all_results] for i in candidate_labels}
    return jsonify({"label": label, "scores": scores})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
