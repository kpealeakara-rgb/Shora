"""Zero-shot LLM scoring of the NaijaScamBench test split via Groq (resumable, batched).

python scripts/eval_llm.py --model openai/gpt-oss-120b --split test --budget 90
python scripts/eval_llm.py --model openai/gpt-oss-120b --split test --report
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shora.benchmark import load_split, score  # noqa: E402
from shora.llm import chat_json  # noqa: E402
from shora.taxonomy import LEGIT_TYPES, SCAM_TYPES  # noqa: E402

BATCH = 10
PROMPT = """You are an expert in Nigerian fraud. For each numbered message decide if it is a SCAM or LEGIT (genuine).
Messages may be in English, Nigerian Pidgin, Yoruba, Igbo or Hausa. Genuine bank alerts, OTP messages that warn not to share,
real delivery/school/utility notices, security advisories and normal family chats are LEGIT.
Also pick the closest type from: {types}.
Return ONLY JSON: {{"results":[{{"i":<number>,"label":"scam"|"legit","type":"<type>"}}]}}

{msgs}"""


def slug(m):
    return re.sub(r"[^a-z0-9]+", "-", m.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/gpt-oss-120b")
    ap.add_argument("--split", default="test")
    ap.add_argument("--budget", type=float, default=90)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    rows = load_split(a.split)
    import random
    order = rows[:]
    random.Random(0).shuffle(order)  # score in random order so partial runs stay representative
    out = ROOT / "benchmark" / "results" / f"llm_{slug(a.model)}_{a.split}_predictions.jsonl"
    done = {}
    if out.exists():
        for l in out.read_text().splitlines():
            d = json.loads(l)
            done[d["id"]] = d
    types = ", ".join(list(SCAM_TYPES) + list(LEGIT_TYPES))
    deadline = time.time() + a.budget
    todo = [r for r in order if r["id"] not in done]
    while todo and not a.report and time.time() < deadline:
        batch = todo[:BATCH]
        msgs = "\n\n".join(f"[{i}] {r['text'][:700]}" for i, r in enumerate(batch))
        try:
            res = chat_json([{"role": "user", "content": PROMPT.format(types=types, msgs=msgs)}], model=a.model,
                            temperature=0.0, max_tokens=1800, deadline=deadline, timeout=45, retries=4)
        except Exception as e:  # noqa: BLE001
            print("fail", str(e)[:120])
            break
        got = {int(x.get("i", -1)): x for x in res.get("results", []) if str(x.get("i", "")).lstrip("-").isdigit()}
        with open(out, "a") as fh:
            for i, r in enumerate(batch):
                x = got.get(i, {})
                d = {"id": r["id"], "pred": (x.get("label") or "").lower() or None, "pred_type": x.get("type")}
                fh.write(json.dumps(d) + "\n")
                done[r["id"]] = d
        todo = [r for r in order if r["id"] not in done]
        print(f"scored {len(done)}/{len(rows)}", flush=True)
    if not todo:
        preds = [done[r["id"]]["pred"] for r in rows]
        tpreds = [done[r["id"]].get("pred_type") or "unknown" for r in rows]
        res = score(rows, preds, tpreds)
        res.update({"model": f"Zero-shot {a.model} (Groq)", "abstained": sum(p not in ("scam", "legit") for p in preds)})
        (ROOT / "benchmark" / "results" / f"llm_{slug(a.model)}_{a.split}.json").write_text(json.dumps(res, indent=2))
        print(res)
    else:
        print(f"remaining {len(todo)}")
        if a.report and done:
            # partial report on the scored subset (e.g. when the Groq daily token quota runs out)
            sub = [r for r in rows if r["id"] in done]
            res = score(sub, [done[r["id"]]["pred"] for r in sub])
            res.update({"model": f"Zero-shot {a.model} (Groq)", "partial": True, "scored": len(sub), "of": len(rows),
                        "subset_ids": [r["id"] for r in sub]})
            (ROOT / "benchmark" / "results" / f"llm_{slug(a.model)}_{a.split}_partial.json").write_text(json.dumps(res, indent=2))
            print({k: v for k, v in res.items() if k != "subset_ids"})


if __name__ == "__main__":
    main()
