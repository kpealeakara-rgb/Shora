# Contributing to Shora

Thank you for helping protect Nigerians from scams. 🇳🇬 There are four ways to help, from easiest to hardest.

## 1. Submit a real scam (or real legit) message ⭐ most valuable

NaijaScam v0.1 is synthetic. Real messages are what will make Shora work in the real world.

**Before you share, remove all personal data.** Replace it like this:

| Replace | With |
|---|---|
| Names of real people | `[NAME]` |
| Phone numbers | `[PHONE]` |
| Account / card / BVN / NIN numbers | `[ACCOUNT]`, `[CARD]`, `[BVN]`, `[NIN]` |
| Email addresses | `[EMAIL]` |
| Home or office addresses | `[ADDRESS]` |

Keep the scammer's **links, brand names, amounts and wording** exactly as they were. Those are the signals.
Never include your own OTP, PIN or password.

Open an issue titled **"Message submission"** and fill in:

```
text:        <the message, PII removed>
label:       scam | legit
scam_type:   (optional) e.g. fake_credit_alert, ponzi_crypto, loan_app_extortion …
language:    en | pcm | yo | ig | ha (or "mixed")
channel:     SMS | WhatsApp | Telegram | email | call | other
month/year:  when you received it
consent:     I received this message myself (or have permission) and removed personal data. I agree it can be released under CC BY 4.0.
```

Screenshots are welcome too, but please blur names, numbers and profile pictures first.

## 2. Review the language quality

Native speakers of **Yorùbá, Igbo, Hausa or Naija Pidgin**: open `data/naijascam/test.csv`, filter by language,
and flag rows that sound unnatural, wrong or mislabelled. Open an issue or a PR editing the JSONL with a short
note. Fixing the offline advice strings in `src/shora/analyze.py` (`VERDICT_WORDS`, `FALLBACK_ADVICE`) is also a
great first PR.

## 3. Improve the models

- Add a model to NaijaScamBench: write predictions for the `test` and `challenge` splits, score them with
  `shora.benchmark.score`, and add your JSON to `benchmark/results/`.
- Add multilingual red-flag rules to `src/shora/rules.py` (with a test).
- Roadmap items in the README (screenshot checker, Whisper voice checker, SEC investment lookup, WhatsApp bot,
  GGUF/ONNX on-device model) are all open for contributors. Comment on an issue before starting a big one.

## 4. Development setup

```bash
pip install -r requirements.txt pytest
python scripts/train_baseline.py
pytest -q
```

Style: keep it simple, standard library + scikit-learn in `src/shora` (torch/transformers only in scripts),
type hints welcome, and every new feature should come with a test.

## Code of conduct

Be kind. Scam victims are not stupid. Don't shame them in issues, examples or docs. Never post content
that helps someone run a scam (working phishing kits, real victims' data, etc.); such issues will be removed.
