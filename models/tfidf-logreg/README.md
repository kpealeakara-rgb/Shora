---
license: mit
language: [en, pcm, yo, ig, ha]
library_name: sklearn
pipeline_tag: text-classification
tags: [scam-detection, fraud, nigeria, tfidf, logistic-regression]
datasets: [Nihilitybot666/naijascam]
metrics: [accuracy, f1]
---

# Shora TF-IDF + LogReg (NaijaScam v0.1)

Tiny (~4 MB) scikit-learn baseline from [Shora](https://github.com/kpealeakara-rgb/shora).
- `binary.joblib`: scam vs legit (word 1–2-gram + char_wb 2–5-gram TF-IDF → logistic regression, C=4, balanced)
- `scam_type.joblib`: same features → 17-way type (9 scam + 8 legit types)

| split | accuracy | macro-F1 |
|---|---:|---:|
| NaijaScam test (365, synthetic, in-distribution) | 97.8 | 97.8 |
| NaijaScam challenge (40, hand-written, OOD) | 75.0 | 73.3 |

Scam-type accuracy on test: 89.3. Speed: ~0.5 ms per message on CPU.

**Caveat:** it misses about half of the short, conversational, hand-written scams (challenge scam recall 50%), so
use it as a fast first pass alongside an LLM or human judgement, not as the only safeguard.

```python
import joblib
clf = joblib.load("binary.joblib")
clf.predict_proba(["Your BVN has been suspended. Send the OTP to reactivate."])  # classes_: ['legit', 'scam']
```
