"""Clean, quality-filter, dedupe and split NaijaScam.

raw (data/raw/*.jsonl) + seeds (data/seeds/seed_messages.py)
  -> data/naijascam/{train,validation,test}.jsonl, test.csv, stats.json
"""
from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "data" / "seeds"))

from seed_messages import SEEDS  # noqa: E402
from shora.taxonomy import SCAM_TYPES  # noqa: E402

OUT = ROOT / "data" / "naijascam"
rng = random.Random(42)

PREFIX = re.compile(r"^\s*(?:\[?\(?)(?:sms|whatsapp(?: broadcast| message)?|telegram(?: message)?|email(?: snippet)?|"
                    r"subject|facebook(?:/instagram)?(?: dm)?|instagram(?: dm)?|x(?: \(twitter\))?(?: dm)?|twitter(?: dm)?|"
                    r"truecaller[^:]{0,25}|dm|from [^:]{1,30})(?:\)?\]?)\s*[:\-–]\s*", re.I)
SHORT = re.compile(r"(bit\.ly|tinyurl|t\.ly|cutt\.ly|is\.gd|rb\.gy|shorturl|goo\.gl|tiny\.cc)", re.I)
ASK_SECRET = re.compile(r"(send|share|give|forward|read|reply with|tell)\b.{0,35}\b(otp|pin|bvn|password|token|puk|cvv|code)\b", re.I)
EN_STOP = set("the a an and or to of in on for is are was be you your we our i it this that with at from by have has will "
              "please kindly dear if not can do my me us as so now get".split())
MARKERS = {
    "pcm": set("dey una abeg wetin wey dem wahala sabi comot abi sef oya don no vex pikin sharp im go make na fit e".split()),
    "yo": set("ni ti mo ẹ e o si fun ati lati awọn awon owo jọwọ jowo yin wa rẹ re kí ki ṣe se mi ko kò bá ba sí lo".split()),
    "ig": set("na ka gị gi m nke ego biko ndewo kedu ya maka bụ bu ga ị i ọ ndị ndi anyị anyi ugbu a nwanne".split()),
    "ha": set("ka da na don ba kuɗi kudi zuwa domin allah dinka ɗinka ya sannu wannan za mu ku a ta shi ga yanzu kana".split()),
}
MASK_PAT = re.compile(r"0\*\*\.\.\.\d{4}")


def rand_mask(_m=None):
    style = rng.randint(0, 3)
    d = lambda n: "".join(str(rng.randint(0, 9)) for _ in range(n))  # noqa: E731
    return [f"{d(2)}******{d(2)}", f"***{d(4)}", f"{d(4)}XXXX{d(2)}", f"0{d(2)}*****{d(3)}"][style]


def clean(t: str) -> str:
    t = t.strip().strip('"“”').strip()
    for _ in range(2):
        t = PREFIX.sub("", t, count=1).strip().strip('"“”').strip()
    t = MASK_PAT.sub(rand_mask, t)
    return re.sub(r"[ \t]+", " ", t)


def toks(t):
    return re.findall(r"[\wẹọṣɗƙịụńǹ']+", t.lower())


def fix_language(r):
    lang = r["language"]
    if lang == "en":
        return lang
    tk = toks(r["text"])
    if not tk:
        return None
    en = sum(w in EN_STOP for w in tk) / len(tk)
    mk = sum(w in MARKERS[lang] for w in tk)
    if lang == "pcm":
        strong = (MARKERS["pcm"] - {"go", "make", "fit"}) | {"wan", "am", "say", "oga", "na", "abi", "wahala"}
        if not any(w in strong for w in tk) and not re.search(r"\b(i be|e fit|no be|make i|make you)\b", r["text"], re.I):
            return "en"
        return lang
    if en > 0.4 and mk < 3:
        return "en"
    return lang


def legit_ok(r):
    t, ty = r["text"], r["scam_type"]
    if ty == "legit_security_advisory":
        return not SHORT.search(t)
    if ty == "legit_otp":
        return not re.search(r"(send|share|forward|give)\s+(me|us|it to|the code to)", t, re.I) and not SHORT.search(t)
    if ASK_SECRET.search(t) and not re.search(r"(never|do not|don't|no go|kar ka|ma ṣe|ma se|ejila)", t, re.I):
        return False
    if SHORT.search(t) and re.search(r"(pay|transfer|send|verify|claim|bvn|otp)", t, re.I):
        return False
    return True


def merge_jobs():
    """Merge data/raw/jobs/*.jsonl (generator output) into the single released raw file."""
    jobs = sorted((ROOT / "data" / "raw" / "jobs").glob("*.jsonl"))
    with open(ROOT / "data" / "raw" / "naijascam_raw_v0.1.jsonl", "w") as out:
        for f in jobs:
            for line in f.read_text().splitlines():
                if line.strip():
                    r = json.loads(line)
                    r["batch"] = f.stem
                    out.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    if "--merge" in sys.argv:
        merge_jobs()
    rows = []
    for f in sorted((ROOT / "data" / "raw").glob("*.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                r.setdefault("batch", f.stem)
                rows.append(r)
    for text, label, ty, lang, flags, ref in SEEDS:
        rows.append({"text": text, "label": label, "scam_type": ty, "language": lang, "red_flags": flags,
                     "source": "seed", "generator": "hand-written", "batch": "seed", "ref": ref})
    n_raw = len(rows)
    drops = Counter()
    kept = []
    for r in rows:
        r["text"] = clean(r["text"])
        if not (15 <= len(r["text"]) <= 1200):
            drops["length"] += 1
            continue
        if r["label"] == "legit" and not legit_ok(r):
            drops["legit_noise"] += 1
            continue
        if r["label"] == "scam" and not r.get("red_flags"):
            drops["scam_no_flags"] += 1
            continue
        lang = fix_language(r)
        if lang is None:
            drops["empty"] += 1
            continue
        if lang != r["language"]:
            drops[f"relabel_{r['language']}_to_{lang}"] += 1
            r["language"] = lang
        r["red_flags"] = [str(x).strip()[:60] for x in r.get("red_flags", []) if str(x).strip()][:5]
        kept.append(r)

    # exact dedupe
    seen, uniq = set(), []
    for r in kept:
        k = re.sub(r"\W+", "", r["text"].lower())
        if k in seen:
            drops["exact_dup"] += 1
            continue
        seen.add(k)
        uniq.append(r)
    # near-dup removal (char n-gram cosine > 0.85)
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1)
    X = vec.fit_transform([r["text"] for r in uniq])
    sims = (X @ X.T).tocsr()
    drop = set()
    for i in range(len(uniq)):
        if i in drop:
            continue
        row = sims.getrow(i)
        for j, s in zip(row.indices, row.data):
            if j > i and s > 0.85 and j not in drop:
                drop.add(j)
    drops["near_dup"] = len(drop)
    final = [r for i, r in enumerate(uniq) if i not in drop]

    for i, r in enumerate(final):
        r["id"] = f"ns-{i:05d}"
    strat = [f"{r['label']}_{r['language']}" for r in final]
    idx = np.arange(len(final))
    tr, te = train_test_split(idx, test_size=0.2, random_state=42, stratify=strat)
    tr, va = train_test_split(tr, test_size=0.125, random_state=42, stratify=[strat[i] for i in tr])
    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["id", "text", "label", "scam_type", "language", "red_flags", "source", "generator"]
    splits = {"train": tr, "validation": va, "test": te}
    for name, ids in splits.items():
        with open(OUT / f"{name}.jsonl", "w") as fh:
            for i in sorted(ids):
                fh.write(json.dumps({c: final[i].get(c) for c in cols}, ensure_ascii=False) + "\n")
    import csv
    with open(OUT / "test.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for i in sorted(te):
            r = final[i]
            w.writerow([r["id"], r["text"], r["label"], r["scam_type"], r["language"], " | ".join(r["red_flags"]),
                        r["source"], r["generator"]])
    stats = {
        "raw": n_raw, "final": len(final), "drops": dict(drops),
        "splits": {k: int(len(v)) for k, v in splits.items()},
        "label": dict(Counter(r["label"] for r in final)),
        "language": dict(Counter(r["language"] for r in final)),
        "scam_type": dict(Counter(r["scam_type"] for r in final)),
        "source": dict(Counter(r["source"] for r in final)),
        "label_by_language": {l: dict(Counter(r["label"] for r in final if r["language"] == l))
                              for l in ["en", "pcm", "yo", "ig", "ha"]},
    }
    (OUT / "stats.json").write_text(json.dumps(stats, indent=2))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
