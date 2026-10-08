"""Fine-tune a small multilingual African transformer (default: Davlan/afro-xlmr-mini) for scam vs legit.

CPU-friendly and resumable: training runs in time-boxed chunks (--budget seconds) and checkpoints
trainable weights + optimizer, so it works on a laptop or a free CI/Space runner.
Embeddings are frozen (they are ~80% of the parameters) to cut compute and memory.

python scripts/finetune_transformer.py --budget 90          # repeat until it prints "training complete"
python scripts/finetune_transformer.py --evaluate           # score the test split
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shora.benchmark import load_split, score  # noqa: E402

torch.set_num_threads(2)
LABELS = ["legit", "scam"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(ROOT / "models" / "hf" / "afro-xlmr-mini"),
                    help="local dir or hub id, e.g. Davlan/afro-xlmr-mini")
    ap.add_argument("--out", default=str(ROOT / "models" / "afro-xlmr-mini-naijascam"))
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--max_len", type=int, default=128)
    ap.add_argument("--budget", type=float, default=90)
    ap.add_argument("--evaluate", action="store_true")
    ap.add_argument("--split", default="test")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    tok = AutoTokenizer.from_pretrained(a.base)
    model = AutoModelForSequenceClassification.from_pretrained(a.base, num_labels=2)
    for p in model.base_model.embeddings.parameters():
        p.requires_grad = False
    trainable = [n for n, p in model.named_parameters() if p.requires_grad]
    ck = out / "checkpoint.pt"
    state = torch.load(ck, weights_only=False) if ck.exists() else None
    if state:
        model.load_state_dict(state["weights"], strict=False)

    if a.evaluate:
        model.eval()
        te = load_split(a.split)
        preds, t0 = [], time.time()
        with torch.no_grad():
            for i in range(0, len(te), 32):
                enc = tok([r["text"] for r in te[i:i + 32]], truncation=True, max_length=a.max_len, padding=True,
                          return_tensors="pt")
                preds += [LABELS[j] for j in model(**enc).logits.argmax(-1).tolist()]
        res = score(te, preds)
        with open(ROOT / "benchmark" / "results" / f"afro_xlmr_mini_{a.split}_predictions.jsonl", "w") as fh:
            for r, p in zip(te, preds):
                fh.write(json.dumps({"id": r["id"], "gold": r["label"], "pred": p}) + "\n")
        res.update({"model": "afro-xlmr-mini fine-tuned (frozen embeddings)", "epochs": a.epochs,
                    "ms_per_message_cpu": round((time.time() - t0) / len(te) * 1000, 1),
                    "train_seconds_total": round(state.get("train_seconds", 0), 1) if state else None})
        (ROOT / "benchmark" / "results" / ("afro_xlmr_mini.json" if a.split == "test" else f"afro_xlmr_mini_{a.split}.json")).write_text(json.dumps(res, indent=2))
        print(res)
        return

    train = load_split("train") + load_split("validation")
    g = torch.Generator().manual_seed(13)
    steps_per_epoch = math.ceil(len(train) / a.bs)
    total = steps_per_epoch * a.epochs
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / (0.1 * total)) * max(0.0, (total - s) / total))
    step, train_s = 0, 0.0
    if state:
        opt.load_state_dict(state["opt"])
        sched.load_state_dict(state["sched"])
        step, train_s = state["step"], state.get("train_seconds", 0.0)
    if step >= total:
        print("training complete", step, total)
        return
    perms = [torch.randperm(len(train), generator=g).tolist() for _ in range(a.epochs)]
    model.train()
    t0 = time.time()
    losses = []
    while step < total and time.time() - t_start < a.budget:
        ep, k = divmod(step, steps_per_epoch)
        idx = perms[ep][k * a.bs:(k + 1) * a.bs]
        batch = [train[i] for i in idx]
        enc = tok([r["text"] for r in batch], truncation=True, max_length=a.max_len, padding=True, return_tensors="pt")
        y = torch.tensor([LABELS.index(r["label"]) for r in batch])
        loss = model(**enc, labels=y).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step(); opt.zero_grad()
        losses.append(loss.item())
        step += 1
    train_s += time.time() - t0
    sd = {n: p for n, p in model.state_dict().items() if n in trainable}
    torch.save({"weights": sd, "opt": opt.state_dict(), "sched": sched.state_dict(), "step": step,
                "train_seconds": train_s}, ck)
    print(f"step {step}/{total} epoch {step / steps_per_epoch:.2f} loss {sum(losses) / max(1, len(losses)):.4f} "
          f"({len(losses)} steps this chunk)")
    if step >= total:
        print("training complete")


if __name__ == "__main__":
    main()
