import os
import asyncio
import aiohttp
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

mdls = [
    "facebook/bart-large-mnli",
    "roberta-large-mnli",
    "MoritzLaurer/deberta-v3-base-mnli-xnli",
    "joeddav/xlm-roberta-large-xnli",
    "typeform/distilbert-base-uncased-mnli",
    "cross-encoder/nli-deberta-v3-large",
    "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    "MoritzLaurer/DeBERTa-v3-large-mnli-xnli",
    "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli",
    "textattack/distilbert-base-uncased-MNLI"
]
lbls = ["Informative", "Promotional", "Opinionated", "Emotional", "Factual", "Neutral", "Academic", "Subjective", "Actionable", "Speculative"]

async def req_mdl(session, mdl, txt):
    url = f"https://api-inference.huggingface.co/models/{mdl}"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    pl = {"inputs": txt, "parameters": {"candidate_labels": lbls}, "options": {"wait_for_model": True}}
    async with session.post(url, json=pl, headers=headers, timeout=35) as r:
        try:
            js = await r.json()
            return js
        except:
            return {}

async def all_res(txt):
    async with aiohttp.ClientSession() as s:
        tasks = [req_mdl(s, mdl, txt) for mdl in mdls]
        res = await asyncio.gather(*tasks)
        return res

def vote_lbl(rlist):
    votes = {}
    for r in rlist:
        if "labels" in r and "scores" in r:
            lbl = r["labels"][0]
            sc = r["scores"][0]
            votes[lbl] = votes.get(lbl, 0) + sc
    if votes:
        return max(votes, key=votes.get), votes
    return "Unknown", {}

@app.route("/classify", methods=["POST"])
def classify():
    d = request.get_json()
    txt = d.get("text", "")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rlist = loop.run_until_complete(all_res(txt))
    lbl, scrs = vote_lbl(rlist)
    return jsonify({"label": lbl, "scores": scrs, "raw": rlist})

if __name__ == "__main__":
    app.run()
