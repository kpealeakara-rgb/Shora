"""Parity check: run the static Space's JS engine (via node) and compare with the sklearn pipeline.

    python scripts/check_static_parity.py            # test split (default)
    python scripts/check_static_parity.py --all      # train + validation + test + challenge

Compares: binary label, scam type, red-flag keys, blended verdict, and max |prob difference|.
Exits non-zero if binary-label or scam-type agreement on the checked set is below 99.5%.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shora.analyze import local_pass  # noqa: E402
from shora.classifier import ShoraClassifier  # noqa: E402
from shora.rules import find_red_flags  # noqa: E402

STATIC = ROOT / "space-static"
NODE_RUNNER = r"""
const fs = require('fs');
const M = require(process.argv[2] + '/model.js');
const { Engine } = require(process.argv[2] + '/shora.js');
const eng = new Engine(M);
const texts = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const t0 = Date.now();
const out = texts.map(t => { const r = eng.predict(t);
  return {label: r.label, p: r.scam_probability, type: r.scam_type, tp: r.type_probability,
          flags: r.red_flags.map(f => f.key), verdict: r.verdict, risk: r.risk}; });
process.stderr.write(`node: ${texts.length} msgs in ${Date.now() - t0} ms\n`);
fs.writeFileSync(process.argv[4], JSON.stringify(out));
"""


def load(split):
    return [json.loads(l) for l in (ROOT / "data" / "naijascam" / f"{split}.jsonl").read_text().splitlines() if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    splits = ["train", "validation", "test", "challenge"] if args.all else ["test"]
    rows = [r for s in splits for r in load(s)]
    texts = [r["text"] for r in rows]

    clf = ShoraClassifier.load()
    py = clf.predict_many(texts)
    with tempfile.TemporaryDirectory() as td:
        inp, outp, runner = Path(td) / "in.json", Path(td) / "out.json", Path(td) / "run.js"
        inp.write_text(json.dumps(texts, ensure_ascii=False))
        runner.write_text(NODE_RUNNER)
        subprocess.run(["node", str(runner), str(STATIC), str(inp), str(outp)], check=True)
        js = json.loads(outp.read_text())

    n = len(texts)
    lab = sum(p.label == j["label"] for p, j in zip(py, js))
    typ = sum(p.scam_type == j["type"] for p, j in zip(py, js))
    flg = sum([f["key"] for f in find_red_flags(t)] == j["flags"] for t, j in zip(texts, js))
    ver = sum(local_pass(t)["verdict"] == j["verdict"] for t, j in zip(texts, js))
    dp = max(abs(p.scam_probability - j["p"]) for p, j in zip(py, js))
    dt = max(abs(p.type_probability - j["tp"]) for p, j in zip(py, js))
    gold = sum(j["label"] == r["label"] for r, j in zip(rows, js))
    res = {
        "splits": splits, "n": n,
        "binary_label_agreement": round(100 * lab / n, 2),
        "scam_type_agreement": round(100 * typ / n, 2),
        "red_flag_agreement": round(100 * flg / n, 2),
        "blended_verdict_agreement": round(100 * ver / n, 2),
        "max_abs_scam_prob_diff": float(f"{dp:.2e}"),
        "max_abs_type_prob_diff": float(f"{dt:.2e}"),
        "js_accuracy_vs_gold_labels": round(100 * gold / n, 2),
    }
    print(json.dumps(res, indent=2))
    for i, (p, j) in enumerate(zip(py, js)):
        if p.label != j["label"] or p.scam_type != j["type"]:
            print("MISMATCH", i, p, j, texts[i][:100])
    ok = lab / n >= 0.995 and typ / n >= 0.995
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
