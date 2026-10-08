"""End-to-end analysis: local classifier (fast first pass) + rule red flags + LLM explanation.

    from shora import analyze
    result = analyze("Your BVN go block today, send OTP...", language="pcm")
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

from .classifier import DEFAULT_MODEL_DIR, ShoraClassifier
from .rules import find_red_flags, heuristic_score
from .taxonomy import ALL_TYPES, LANGUAGES, SCAM_TYPES

VERDICT_WORDS = {
    "en": {"scam": "Likely SCAM", "suspicious": "Suspicious - be careful", "legit": "Looks safe"},
    "pcm": {"scam": "E be like SCAM", "suspicious": "Something no clear - shine your eye", "legit": "E be like say e safe"},
    "yo": {"scam": "Ó dàbí ÌTÀN-ÀRÍNRÌN (scam)", "suspicious": "Ẹ ṣọ́ra - ó ní ìfura", "legit": "Ó dàbí pé kò léwu"},
    "ig": {"scam": "Ọ dị ka AGHỤGHỌ (scam)", "suspicious": "Kpachara anya - enwere obi abụọ", "legit": "Ọ dị ka ọ dị mma"},
    "ha": {"scam": "Da alama ZAMBA ce (scam)", "suspicious": "Ka yi hankali - akwai shakka", "legit": "Da alama babu matsala"},
}

FALLBACK_ADVICE = {
    "en": "Do not share any OTP, PIN, BVN or password. Do not click links or pay anyone until you confirm through your bank's "
          "official app or the number on the back of your card.",
    "pcm": "No give anybody your OTP, PIN, BVN or password. No click link or pay money until you confirm am for your bank app "
           "or the number wey dey back of your card.",
    "yo": "Ẹ má ṣe fún ẹnikẹ́ni ní OTP, PIN, BVN tàbí password yín. Ẹ má tẹ link tàbí san owó títí ẹ ó fi jẹ́rìí sí i "
          "nípasẹ̀ app banki yín.",
    "ig": "Enyela onye ọ bụla OTP, PIN, BVN ma ọ bụ password gị. Apịala link ma ọ bụ kwụọ ụgwọ ruo mgbe i kwadoro ya "
          "site na app ụlọ akụ gị.",
    "ha": "Kada ka ba kowa OTP, PIN, BVN ko password ɗinka. Kada ka danna link ko ka biya kuɗi sai ka tabbatar ta "
          "manhajar bankinka.",
}

SYSTEM = """You are Shora (Ṣọ́ra), a Nigerian anti-scam assistant. You judge a single message a user received and explain it
for an ordinary Nigerian (market trader, student, parent). Be precise: genuine bank alerts, OTPs that say "do not share",
delivery updates and family chats are LEGIT. Messages that ask for OTP/PIN/BVN, promise guaranteed returns, demand upfront
fees, threaten to block accounts or shame you, or push you to release goods on an unconfirmed transfer are SCAMS.
Scam types: {types}.
Reply ONLY with JSON: {{"verdict":"scam|suspicious|legit","scam_type":"<one type key or legit_*>","confidence":0-1,
"red_flags":["short phrase in the output language", ...],"explanation":"2-4 simple sentences in the output language",
"what_to_do":"1-2 practical steps in the output language (e.g. call bank on official number, report to EFCC/ FCCPC/ NCC)"}}"""


@lru_cache(maxsize=1)
def _classifier(model_dir: str | None = None):
    model_dir = model_dir or os.environ.get("SHORA_MODEL_DIR", str(DEFAULT_MODEL_DIR))
    try:
        return ShoraClassifier.load(model_dir)
    except Exception:  # model not trained yet
        return None


def local_pass(text: str) -> dict:
    clf = _classifier()
    flags = find_red_flags(text)
    h = heuristic_score(text)
    if clf is None:
        p, st, tp = h, ("unknown" if h < 0.5 else "suspicious"), 0.0
    else:
        pred = clf.predict(text)
        p, st, tp = pred.scam_probability, pred.scam_type, pred.type_probability
    # blend: model dominates, rules nudge
    risk = 0.8 * p + 0.2 * h if clf is not None else h
    verdict = "scam" if risk >= 0.6 else ("suspicious" if risk >= 0.35 else "legit")
    return {"risk": round(float(risk), 3), "model_scam_probability": round(float(p), 3), "verdict": verdict,
            "scam_type": st, "type_probability": round(float(tp), 3), "rule_flags": flags}


def llm_pass(text: str, language: str, hint: dict | None = None, model: str | None = None) -> dict:
    from .llm import DEFAULT_MODEL, chat_json
    types = ", ".join(list(SCAM_TYPES) + ["legit_*"])
    user = (f"Output language: {LANGUAGES.get(language, 'English')}.\n"
            f"Fast local model hint (may be wrong): {json.dumps(hint or {}, ensure_ascii=False)[:600]}\n"
            f"Message:\n<<<\n{text[:3000]}\n>>>")
    return chat_json([{"role": "system", "content": SYSTEM.format(types=types)}, {"role": "user", "content": user}],
                     model=model or DEFAULT_MODEL, temperature=0.2, max_tokens=1200, retries=3)


def analyze(text: str, language: str = "en", use_llm: bool | None = None) -> dict:
    """Return verdict, scam type, red flags and a plain-language explanation."""
    language = language if language in LANGUAGES else "en"
    local = local_pass(text)
    if use_llm is None:
        use_llm = bool(os.environ.get("GROQ_API_KEY"))
    result = {"language": language, "local": local, "engine": "local"}
    if use_llm:
        try:
            hint = {k: local[k] for k in ("verdict", "scam_type", "model_scam_probability")}
            hint["rule_flags"] = [f["flag"] for f in local["rule_flags"]]
            llm = llm_pass(text, language, hint)
            result.update({"verdict": llm.get("verdict", local["verdict"]), "scam_type": llm.get("scam_type", local["scam_type"]),
                           "confidence": llm.get("confidence"), "red_flags": llm.get("red_flags", []),
                           "explanation": llm.get("explanation", ""), "what_to_do": llm.get("what_to_do", ""),
                           "engine": "local+llm"})
            return result
        except Exception as e:  # noqa: BLE001 - fall back to offline explanation
            result["llm_error"] = str(e)[:200]
    v = local["verdict"]
    st = local["scam_type"]
    name = ALL_TYPES.get(st, (st,))[0]
    result.update({
        "verdict": v, "scam_type": st, "confidence": local["risk"] if v != "legit" else 1 - local["risk"],
        "red_flags": [f["flag"] for f in local["rule_flags"]],
        "explanation": (f"{VERDICT_WORDS[language][v]}. Pattern: {name}." if v != "legit"
                        else f"{VERDICT_WORDS[language][v]}."),
        "what_to_do": FALLBACK_ADVICE[language],
    })
    return result
