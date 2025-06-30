from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

model_names = [
    "facebook/bart-large-mnli",
    "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    "typeform/distilbert-base-uncased-mnli",
    "roberta-large-mnli",
    "joeddav/xlm-roberta-large-xnli",
    "cross-encoder/nli-deberta-v3-base",
    "ynie/xlnet-large-cased-xnli",
    "facebook/deberta-v3-large-mnli",
    "textattack/roberta-base-MNLI",
    "vicgalle/xlm-roberta-large-xnli-anli"
]

pipelines = [
    pipeline("zero-shot-classification", model=name)
    for name in model_names
]

context_labels = [
    "Informative", "Promotional", "Opinionated", "Emotional",
    "Academic", "Actionable", "Personal", "News", "Commercial", "Technical"
]

@app.route('/api/nli', methods=['POST'])
def classify():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({"label": "Unknown", "scores": {}})
    votes = {}
    scores_total = {label: 0.0 for label in context_labels}
    for nli in pipelines:
        output = nli(text, context_labels)
        label = output['labels'][0]
        votes[label] = votes.get(label, 0) + 1
        for l, s in zip(output['labels'], output['scores']):
            scores_total[l] += s
    max_vote = max(votes.values())
    top_labels = [l for l, v in votes.items() if v == max_vote]
    if len(top_labels) == 1:
        final_label = top_labels[0]
    else:
        final_label = max(top_labels, key=lambda l: scores_total[l])
    scores_avg = {l: round(scores_total[l]/len(pipelines), 4) for l in context_labels}
    return jsonify({"label": final_label, "scores": scores_avg})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
