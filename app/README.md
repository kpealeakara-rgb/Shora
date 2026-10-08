---
title: Shora — Nigerian Scam Shield
emoji: 🛡️
colorFrom: green
colorTo: red
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: mit
short_description: Check SMS/WhatsApp messages for Nigerian scams in 5 languages
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

# 🛡️ Shora (Ṣọ́ra) — "be careful"

Paste a message you received (SMS, WhatsApp, email). Shora gives a verdict, the likely scam type, the red flags,
and a plain explanation in **English, Naija Pidgin, Yorùbá, Igbo or Hausa**.

- **Fast first pass:** a tiny TF-IDF + logistic-regression model trained on NaijaScam v0.1 (runs in < 1 ms on CPU).
- **Explanation:** an LLM via Groq (set the `GROQ_API_KEY` secret in the Space settings). Without the key, the
  app still works offline with rule-based red flags and templated advice.

Never paste your PIN, OTP or password into any website — including this one.

Source: https://github.com/kpealeakara-rgb/shora · MIT licence.

### Deploying this Space
From the repo root run `bash scripts/prepare_space.sh`, then push the `space/` folder to a new Gradio Space.
