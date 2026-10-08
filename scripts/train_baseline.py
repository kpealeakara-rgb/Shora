"""Train the TF-IDF + LogReg baseline (and score a rules-only baseline) on NaijaScam.

python scripts/train_baseline.py  ->  models/tfidf-logreg/, benchmark/results/*.json
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from sklearn.metrics import f1_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shora.benchmark import load_split, score  # noqa: E402
from shora.classifier import ShoraClassifier  # noqa: E402
from shora.rules import heuristic_score  # noqa: E402

RES = ROOT / "benchmark" / "results"


def main():
    RES.mkdir(parents=True, exist_ok=True)
    tr, va, te = load_split("train"), load_split("validation"), load_split("test")
    X = lambda rows: [r["text"] for r in rows]  # noqa: E731

    # rules-only baseline (threshold tuned on validation)
    best_t, best_f = 0.5, -1
    for t in [i / 20 for i in range(1, 20)]:
        f = f1_score([r["label"] for r in va], ["scam" if heuristic_score(r["text"]) >= t else "legit" for r in va],
                     average="macro")
        if f > best_f:
            best_t, best_f = t, f
    rules_res = score(te, ["scam" if heuristic_score(r["text"]) >= best_t else "legit" for r in te])
    rules_res.update({"model": "Rules only (regex red flags)", "threshold": best_t})
    (RES / "rules.json").write_text(json.dumps(rules_res, indent=2))
    print("rules", rules_res)

    # tf-idf + logreg, C tuned on validation
    best = None
    for C in [1, 4, 8, 16, 32]:
        clf = ShoraClassifier.train(X(tr), [r["label"] for r in tr], [r["scam_type"] for r in tr], C=C)
        preds = [p.label for p in clf.predict_many(X(va))]
        f = f1_score([r["label"] for r in va], preds, average="macro")
        print(f"C={C} val macro-F1={f:.4f}")
        if best is None or f > best[0]:
            best = (f, C)
    C = best[1]
    t0 = time.time()
    trva = tr + va
    clf = ShoraClassifier.train(X(trva), [r["label"] for r in trva], [r["scam_type"] for r in trva], C=C)
    train_s = time.time() - t0
    t0 = time.time()
    preds = clf.predict_many(X(te))
    infer_ms = (time.time() - t0) / len(te) * 1000
    res = score(te, [p.label for p in preds], [p.scam_type for p in preds])
    res.update({"model": "TF-IDF (word+char) + LogReg", "C": C, "train_seconds": round(train_s, 1),
                "ms_per_message_cpu": round(infer_ms, 2)})
    clf.meta.update({"C": C, "val_macro_f1": round(best[0], 4), "test": res})
    clf.save()
    (RES / "tfidf_logreg.json").write_text(json.dumps(res, indent=2))
    with open(RES / "tfidf_logreg_test_predictions.jsonl", "w") as fh:
        for r, p in zip(te, preds):
            fh.write(json.dumps({"id": r["id"], "gold": r["label"], "pred": p.label, "p_scam": round(p.scam_probability, 4),
                                 "gold_type": r["scam_type"], "pred_type": p.scam_type}) + "\n")
    print("tfidf", res)


if __name__ == "__main__":
    main()
