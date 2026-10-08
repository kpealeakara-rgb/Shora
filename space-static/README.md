---
title: Shora
emoji: 🛡️
colorFrom: green
colorTo: yellow
sdk: static
pinned: false
license: mit
short_description: Offline Nigerian scam checker in 5 languages, in-browser
tags:
  - scam-detection
  - fraud
  - nigeria
  - pidgin
  - yoruba
  - igbo
  - hausa
datasets:
  - Nihilitybot666/naijascam
---

# 🛡️ Shora (Ṣọ́ra): "be careful"

Paste a message you received (SMS, WhatsApp, email). Shora gives a **verdict with a scam probability**, the
**likely scam type**, the **red flags** it matched, and short **safety advice in English, Naija Pidgin, Yorùbá,
Igbo or Hausa**.

**Everything runs in your browser.** There is no server: the model and rules are plain JavaScript files, so
nothing you paste leaves your phone.

## How it works
- `model.js`: the shipped TF-IDF (word 1-2 grams + char_wb 2-5 grams) + logistic-regression model from the
  Shora repo, exported by `scripts/export_static.py` (shared vocabulary, integer document frequencies, int16
  coefficients with a per-class scale).
- `shora.js`: a line-by-line re-implementation of the sklearn pipeline and the regex red-flag rules.
  Parity with sklearn on the full NaijaScam test set (365 messages): **100%** identical labels and scam types,
  max probability difference about 3e-5 (`scripts/check_static_parity.py`).
- `i18n.js`: pre-written UI text and advice per scam type in five languages.
- `index.html` / `app.js`: the page. No build step, no external CDNs.

Model: trained on NaijaScam v0.1 (synthetic, grounded in public warnings), 97.8% test accuracy. It can be wrong,
especially on short, conversational scams. Always confirm with your bank's official number.

Never paste your PIN, OTP or password into any website, including this one.

Code: https://github.com/kpealeakara-rgb/Shora · Dataset: https://huggingface.co/datasets/Nihilitybot666/naijascam · MIT licence.
