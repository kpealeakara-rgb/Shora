"""Export the shipped TF-IDF + LogReg models and the red-flag rules to a compact JS file for the static Space.

    python scripts/export_static.py            # writes space-static/model.js

What is exported (both heads share one vocabulary because they were fit on the same texts):
  * word + char_wb vocabularies (ordered by feature index) and document frequencies (ints; idf is
    recomputed in JS exactly as sklearn does: ln((1+n)/(1+df)) + 1)
  * LogReg coefficients quantised to int16 with one scale per class row, plus intercepts and classes
  * every rule in src/shora/rules.py, with Python-regex syntax translated to an equivalent JS (u-flag) regex
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shora.rules import RULES, SAFE_HINTS  # noqa: E402

MODEL_DIR = ROOT / "models" / "tfidf-logreg"
OUT = ROOT / "space-static" / "model.js"

# --- Python `re` (unicode str pattern) -> JS RegExp with the `u` flag -------------------------------
W = r"\p{L}\p{N}_"         # Python \w for str patterns == [\p{L}\p{N}_] (checked over all code points)
PY_SPACE = r" \t\n\r\f\v\x1c-\x1f\x85\xa0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000"


def translate(p: str) -> str:
    """Translate the subset of Python regex syntax used by rules.py into JS-with-u semantics.

    Differences handled: \\b, \\w, \\W, \\d, \\s, \\S and `.` (Python's `.` matches \\r; JS's does not).
    """
    out, i, in_class = [], 0, False
    while i < len(p):
        c = p[i]
        if c == "\\" and i + 1 < len(p):
            n = p[i + 1]
            i += 2
            if n == "w":
                out.append(W if in_class else f"[{W}]")
            elif n == "W":
                if in_class:
                    raise ValueError("\\W inside class not supported")
                out.append(f"[^{W}]")
            elif n == "d":
                out.append(r"\p{Nd}" if in_class else r"[\p{Nd}]")
            elif n == "s":
                out.append(PY_SPACE if in_class else f"[{PY_SPACE}]")
            elif n == "S":
                if in_class:
                    raise ValueError("\\S inside class not supported")
                out.append(f"[^{PY_SPACE}]")
            elif n == "b":
                if in_class:
                    raise ValueError("\\b inside class not supported")
                out.append(f"(?:(?<=[{W}])(?![{W}])|(?<![{W}])(?=[{W}]))")
            else:
                out.append("\\" + n)
            continue
        if in_class:
            if c == "]":
                in_class = False
            out.append(c)
        elif c == "[":
            in_class = True
            out.append(c)
            if i + 1 < len(p) and p[i + 1] == "^":
                out.append("^")
                i += 1
        elif c == ".":
            out.append(r"[^\n]")
        else:
            out.append(c)
        i += 1
    return "".join(out)


def b64_i16(a: np.ndarray) -> str:
    return base64.b64encode(a.astype("<i2").tobytes()).decode("ascii")


def quantise(rows: np.ndarray):
    scales = np.abs(rows).max(axis=1) / 32767.0
    scales[scales == 0] = 1.0
    q = np.round(rows / scales[:, None]).astype(np.int16)
    return q, scales


def main():
    binary = joblib.load(MODEL_DIR / "binary.joblib")
    typer = joblib.load(MODEL_DIR / "scam_type.joblib")
    meta = json.loads((MODEL_DIR / "meta.json").read_text())

    vecs = {}
    for (name, vb), (_, vt) in zip(binary.named_steps["features"].transformer_list,
                                   typer.named_steps["features"].transformer_list):
        assert vb.vocabulary_ == vt.vocabulary_ and np.allclose(vb.idf_, vt.idf_), "heads must share vocab"
        p = vb.get_params()
        assert p["lowercase"] and p["sublinear_tf"] and p["norm"] == "l2" and p["smooth_idf"] and p["use_idf"]
        assert p["strip_accents"] is None and p["preprocessor"] is None and p["tokenizer"] is None
        assert p["token_pattern"] == r"(?u)\b\w\w+\b" and p["stop_words"] is None
        vocab = [None] * len(vb.vocabulary_)
        for term, idx in vb.vocabulary_.items():
            vocab[idx] = term
        n = meta["n_train"]
        df = (1 + n) / np.exp(vb.idf_ - 1) - 1
        dfi = np.round(df).astype(int)
        assert np.abs(df - dfi).max() < 1e-6, "could not recover integer df"
        assert np.allclose(np.log((1 + n) / (1 + dfi)) + 1, vb.idf_, atol=1e-12)
        vecs[name] = {"analyzer": p["analyzer"], "ngram": list(p["ngram_range"]), "vocab": vocab, "df": dfi.tolist()}
    assert binary.named_steps["features"].transformer_weights is None

    cb, ct = binary.named_steps["clf"], typer.named_steps["clf"]
    assert list(cb.classes_) == ["legit", "scam"] and cb.coef_.shape[0] == 1
    qb, sb = quantise(cb.coef_)
    qt, st = quantise(ct.coef_)

    rules = [{"key": r.key, "flag": r.flag, "weight": r.weight, "re": translate(r.pattern.pattern)} for r in RULES]
    safe = [translate(p.pattern) for p in SAFE_HINTS]

    model = {
        "version": "tfidf-logreg v0.1 (NaijaScam v0.1)",
        "n": meta["n_train"],
        "word": vecs["word"], "char": vecs["char"],
        "binary": {"classes": list(cb.classes_), "intercept": cb.intercept_.tolist(),
                   "scales": sb.tolist(), "coef": b64_i16(qb.ravel())},
        "type": {"classes": list(ct.classes_), "intercept": ct.intercept_.tolist(),
                 "scales": st.tolist(), "coef": b64_i16(qt.ravel())},
        "rules": rules, "safe_hints": safe,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    js = "/* Generated by scripts/export_static.py: do not edit by hand. */\n" \
         "var SHORA_MODEL = " + json.dumps(model, ensure_ascii=False, separators=(",", ":")) + ";\n" \
         "if (typeof module !== 'undefined') module.exports = SHORA_MODEL;\n"
    OUT.write_text(js, encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size/1e6:.2f} MB): word={len(vecs['word']['vocab'])} "
          f"char={len(vecs['char']['vocab'])} features, {len(rules)} rules")


if __name__ == "__main__":
    main()
