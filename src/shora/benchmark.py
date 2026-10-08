"""NaijaScamBench metrics: accuracy, macro-F1 and per-language F1 on the held-out test split."""
from __future__ import annotations

import json
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score

LANG_ORDER = ["en", "pcm", "yo", "ig", "ha"]
DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "naijascam"


def load_split(name: str, data_dir: Path = DATA_DIR) -> list[dict]:
    return [json.loads(l) for l in (Path(data_dir) / f"{name}.jsonl").read_text().splitlines() if l.strip()]


def score(rows: list[dict], preds: list[str], type_preds: list[str] | None = None) -> dict:
    """rows: gold test rows; preds: 'scam'/'legit' per row (None = abstain, counted wrong)."""
    gold = [r["label"] for r in rows]
    p = [x if x in ("scam", "legit") else ("legit" if g == "scam" else "scam") for x, g in zip(preds, gold)]
    out = {"n": len(rows), "accuracy": accuracy_score(gold, p), "macro_f1": f1_score(gold, p, average="macro"),
           "scam_f1": f1_score(gold, p, pos_label="scam"), "per_language_macro_f1": {}}
    for lang in LANG_ORDER:
        idx = [i for i, r in enumerate(rows) if r["language"] == lang]
        if idx:
            out["per_language_macro_f1"][lang] = f1_score([gold[i] for i in idx], [p[i] for i in idx], average="macro")
    if type_preds is not None:
        gt = [r["scam_type"] for r in rows]
        out["scam_type_accuracy"] = accuracy_score(gt, type_preds)
        out["scam_type_macro_f1"] = f1_score(gt, type_preds, average="macro")
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()} | {
        "per_language_macro_f1": {k: round(v, 4) for k, v in out["per_language_macro_f1"].items()}}
