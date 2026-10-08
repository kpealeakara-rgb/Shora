"""Score the local models (rules, TF-IDF+LogReg) on any split, e.g. the hand-written challenge set.

python scripts/eval_local.py --split challenge
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shora.benchmark import load_split, score  # noqa: E402
from shora.classifier import ShoraClassifier  # noqa: E402
from shora.rules import heuristic_score  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--split", default="challenge")
a = ap.parse_args()
rows = load_split(a.split)
res_dir = ROOT / "benchmark" / "results"
thr = json.loads((res_dir / "rules.json").read_text())["threshold"]
rules = score(rows, ["scam" if heuristic_score(r["text"]) >= thr else "legit" for r in rows]) | {"model": "Rules only"}
clf = ShoraClassifier.load()
preds = clf.predict_many([r["text"] for r in rows])
tf = score(rows, [p.label for p in preds]) | {"model": "TF-IDF (word+char) + LogReg"}
for name, res in (("rules", rules), ("tfidf_logreg", tf)):
    (res_dir / f"{name}_{a.split}.json").write_text(json.dumps(res, indent=2))
    print(name, res)
with open(res_dir / f"tfidf_logreg_{a.split}_predictions.jsonl", "w") as fh:
    for r, p in zip(rows, preds):
        fh.write(json.dumps({"id": r["id"], "gold": r["label"], "pred": p.label, "p_scam": round(p.scam_probability, 4)}) + "\n")
errs = [(r["id"], r["label"], round(p.scam_probability, 2), r["text"][:90]) for r, p in zip(rows, preds) if p.label != r["label"]]
print("TF-IDF errors:")
for e in errs:
    print(" ", e)
