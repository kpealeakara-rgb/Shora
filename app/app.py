"""Shora (Ṣọ́ra) — Gradio app. Hugging Face Space-ready.

Local classifier gives an instant verdict; if GROQ_API_KEY is set (Space secret), an LLM writes the
explanation in English, Pidgin, Yoruba, Igbo or Hausa.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (HERE / "src", HERE.parent / "src"):  # works in the repo and inside a flattened Space
    if p.exists():
        sys.path.insert(0, str(p))
if (HERE / "models" / "tfidf-logreg").exists():
    os.environ.setdefault("SHORA_MODEL_DIR", str(HERE / "models" / "tfidf-logreg"))

import gradio as gr  # noqa: E402

from shora import analyze  # noqa: E402
from shora.taxonomy import ALL_TYPES  # noqa: E402

LANG_CHOICES = [("English", "en"), ("Naija Pidgin", "pcm"), ("Yorùbá", "yo"), ("Igbo", "ig"), ("Hausa", "ha")]
BADGE = {"scam": ("🚨", "#c62828"), "suspicious": ("⚠️", "#ef6c00"), "legit": ("✅", "#2e7d32")}
EXAMPLES = [
    ["Dear customer, your BVN has been restricted by CBN. Click bit.ly/bvn-ng24 to update within 24hrs or your account will be blocked.", "en"],
    ["Oga I don send the N85,000. Na network delay, e go reflect. Abeg release the goods make my driver carry am sharp sharp.", "pcm"],
    ["Join our AI trading platform, 10% daily profit guaranteed, no risk. Withdrawal open after you pay 5% tax.", "en"],
    ["Ẹ fi ₦50,000 sí platform AI trading wa, ẹ máa gba ₦5,000 lójoojúmọ́. Kò sí ewu rárá.", "yo"],
    ["Acct:01******89 Amt:NGN5,000.00 DR Desc:NIP/TRF TO ADEBAYO T Date:08-Oct-26 Avail Bal:NGN43,210.50", "en"],
    ["Mama, I don reach hostel o. I go call you after lecture tomorrow. Greet Papa for me.", "pcm"],
]


def run(text: str, lang: str):
    if not text or not text.strip():
        return "Paste a message to check.", "", ""
    r = analyze(text.strip(), language=lang)
    icon, color = BADGE.get(r["verdict"], ("❔", "#555"))
    tname = ALL_TYPES.get(r.get("scam_type"), (r.get("scam_type") or "-",))[0]
    loc = r["local"]
    head = (f"<div style='padding:14px;border-radius:12px;background:{color};color:white;font-size:1.3em'>"
            f"{icon} <b>{r['verdict'].upper()}</b> · {tname}</div>"
            f"<p style='opacity:.75;font-size:.9em'>Fast local model: {loc['model_scam_probability']:.0%} scam probability "
            f"· engine: {r['engine']}</p>")
    flags = "\n".join(f"- {f}" for f in (r.get("red_flags") or [])) or "- No strong red flags found."
    body = f"**Why:** {r.get('explanation', '')}\n\n**What to do:** {r.get('what_to_do', '')}"
    return head, flags, body


with gr.Blocks(title="Shora — Nigerian Scam Shield") as demo:
    gr.Markdown("# 🛡️ Shora (Ṣọ́ra) — *be careful*\nPaste any SMS, WhatsApp or email you received. Shora checks it "
                "for Nigerian scam patterns (fake alerts, BVN/OTP theft, Ponzi 'AI trading', loan-app threats, fake jobs, "
                "grants...) and explains in your language. **Never paste your PIN, OTP or password.**")
    with gr.Row():
        with gr.Column(scale=3):
            msg = gr.Textbox(lines=6, label="Message", placeholder="Paste the message here…")
            lang = gr.Radio(LANG_CHOICES, value="en", label="Explain in")
            btn = gr.Button("Check message", variant="primary")
        with gr.Column(scale=3):
            verdict = gr.HTML()
            flags = gr.Markdown(label="Red flags")
            expl = gr.Markdown()
    gr.Examples(EXAMPLES, [msg, lang])
    btn.click(run, [msg, lang], [verdict, flags, expl])
    msg.submit(run, [msg, lang], [verdict, flags, expl])
    gr.Markdown("Open source (MIT) · dataset: NaijaScam v0.1 (synthetic, grounded in public warnings) · "
                "Shora can be wrong: always confirm with your bank's official number.")

if __name__ == "__main__":
    demo.launch()
