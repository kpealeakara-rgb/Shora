"""Generate synthetic-but-grounded NaijaScam messages with Groq.

Resumable: each (type, language, k) job writes data/raw/<job>.jsonl and is skipped if present.
Usage: python scripts/generate_dataset.py --budget 100   # seconds to keep launching jobs
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shora.llm import chat_json  # noqa: E402
from shora.taxonomy import LANGUAGES, LEGIT_TYPES, SCAM_TYPES  # noqa: E402

RAW = ROOT / "data" / "raw" / "jobs"  # one file per generation job (merge with scripts/build_dataset.py --merge)
PER_CALL = 12
CALLS_PER_LANG = {"en": 3, "pcm": 3, "yo": 1, "ig": 1, "ha": 1}

LANG_GUIDE = {
    "en": "Nigerian English as really typed in SMS/WhatsApp (some abbreviations, 'pls', 'kindly', 'urgently', occasional typos).",
    "pcm": "Authentic Nigerian Pidgin (e.g. 'abeg', 'wetin', 'una', 'dey', 'no vex', 'na im', 'make you', 'oya', 'sharp sharp'), "
           "NOT English with one pidgin word. Bank/tech words may stay English.",
    "yo": "Yoruba as Nigerians type it on phones: mostly Yoruba sentences (with or without tone marks, vary it), natural code-mixing "
          "of English banking/tech words (BVN, OTP, account, link, transfer). Do not translate brand names.",
    "ig": "Igbo as Nigerians type it on phones: mostly Igbo sentences (diacritics optional, vary it), natural code-mixing with "
          "English banking/tech words. Do not translate brand names.",
    "ha": "Hausa as Nigerians type it on phones (Kano/Kaduna/Abuja style), mostly Hausa sentences with natural English code-mixing "
          "for banking/tech words. Do not translate brand names.",
}

CHANNELS = ["SMS", "WhatsApp message", "WhatsApp broadcast", "Telegram message", "Facebook/Instagram DM", "email snippet",
            "X (Twitter) DM", "Truecaller-labelled SMS"]
BANKS = ["GTBank", "Access Bank", "Zenith Bank", "UBA", "First Bank", "Fidelity", "Union Bank", "Sterling", "Wema/ALAT",
         "Stanbic IBTC", "FCMB", "Ecobank", "Polaris", "Kuda", "OPay", "Moniepoint", "Palmpay", "Paga", "Carbon", "FairMoney"]
CITIES = ["Lagos", "Abuja", "Ibadan", "Kano", "Port Harcourt", "Enugu", "Onitsha", "Aba", "Benin", "Kaduna", "Akure",
          "Abeokuta", "Jos", "Owerri", "Ilorin", "Warri", "Uyo", "Sokoto", "Maiduguri", "Ado-Ekiti"]


def jobs():
    out = []
    types = [(k, True, v[1]) for k, v in SCAM_TYPES.items()] + [(k, False, v[1]) for k, v in LEGIT_TYPES.items()]
    for t, scam, desc in types:
        for lang, n in CALLS_PER_LANG.items():
            for k in range(n):
                out.append({"id": f"{t}__{lang}__{k}", "type": t, "scam": scam, "desc": desc, "lang": lang, "k": k})
    return out


def build_prompt(job, rng: random.Random):
    banks = ", ".join(rng.sample(BANKS, 4))
    cities = ", ".join(rng.sample(CITIES, 3))
    chans = ", ".join(rng.sample(CHANNELS, 3))
    kind = "SCAM" if job["scam"] else "LEGITIMATE (non-scam)"
    extra = (
        "Make about a third of them SUBTLE (no obvious link, polite tone, realistic sender names, plausible amounts) so they are hard "
        "to catch; the rest can be typical. Every item must be clearly a scam to an expert. Each item needs 2-4 short red_flags (max 6 words each), in English."
        if job["scam"] else
        "Make about a third of them HARD NEGATIVES: genuine messages that mention money, urgency, codes, accounts or even the word "
        "scam/fraud but are completely normal and safe. A legitimate message must NEVER ask the reader to share an OTP/PIN/BVN/password, "
        "click an unknown short link, or pay a stranger. red_flags must be an empty list []."
    )
    sys_msg = ("You build a research dataset to train a scam-detection model protecting Nigerians. You write realistic "
               "example messages. Use fake but realistic details: names, masked account numbers like 0**...4521, naira amounts "
               "(N, NGN or ₦ with commas), Nigerian phone numbers (080x/081x/070x/090x/091x with fake digits), fake short links.")
    user = f"""Write {PER_CALL} distinct {kind} messages of this type:
TYPE: {job['type']} — {job['desc']}
LANGUAGE: {LANGUAGES[job['lang']]}. {LANG_GUIDE[job['lang']]}
Mix channels ({chans}). Where relevant use institutions like {banks}; places like {cities}.
Vary length (1 line to 6 lines), sender persona, tone, amounts and formatting. No two messages should share a template. Write ONLY the message body: do not prefix it with the channel name
(no "SMS:", "WhatsApp:"). Vary masked account formats (e.g. 01******89, ***4521, 2034XXXX17) and never reuse the same digits.
EVERY message must be written in the requested language (code-mixing allowed), not in plain English.
{extra}
Return ONLY JSON: {{"items":[{{"text":"...","red_flags":["..."]}}]}}"""
    return [{"role": "system", "content": sys_msg}, {"role": "user", "content": user}]


def run_job(job, deadline):
    rng = random.Random(hash(job["id"]) & 0xFFFFFFFF)
    data = chat_json(build_prompt(job, rng), temperature=1.0, max_tokens=3000, deadline=deadline + 60)
    items = data.get("items", [])
    rows = []
    for it in items:
        text = (it.get("text") or "").strip()
        if not text:
            continue
        rows.append({"text": text, "label": "scam" if job["scam"] else "legit", "scam_type": job["type"],
                     "language": job["lang"], "red_flags": it.get("red_flags") or [] if job["scam"] else [],
                     "source": "synthetic", "generator": "groq/openai/gpt-oss-120b"})
    if len(rows) < 4:
        raise RuntimeError(f"too few items ({len(rows)})")
    (RAW / f"{job['id']}.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return job["id"], len(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=float, default=95)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    RAW.mkdir(parents=True, exist_ok=True)
    todo = [j for j in jobs() if not (RAW / f"{j['id']}.jsonl").exists()]
    random.Random(0).shuffle(todo)
    deadline = time.time() + a.budget
    print(f"{len(todo)} jobs pending")
    done = 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        futs = {}
        it = iter(todo)
        for _ in range(a.workers):
            j = next(it, None)
            if j:
                futs[ex.submit(run_job, j, deadline)] = j
        while futs:
            fin, _ = cf.wait(futs, return_when=cf.FIRST_COMPLETED)
            for f in fin:
                j = futs.pop(f)
                try:
                    jid, n = f.result()
                    done += 1
                    print("ok", jid, n, flush=True)
                except Exception as e:  # noqa: BLE001
                    print("fail", j["id"], str(e)[:120], flush=True)
                if time.time() < deadline:
                    nj = next(it, None)
                    if nj:
                        futs[ex.submit(run_job, nj, deadline)] = nj
    left = len([j for j in jobs() if not (RAW / f"{j['id']}.jsonl").exists()])
    print(f"done this run: {done}; remaining: {left}")


if __name__ == "__main__":
    main()
