# Shora v1 — build progress log

- 2026-10-08 21:40 WAT — Started. Sandbox: 2 CPU, 7 GB RAM, no GPU, no torch. Installed scikit-learn, pandas, gradio, pytest.
- Groq: only `openai/gpt-oss-120b` is enabled for this key (gpt-oss-20b, qwen3.8-27b, safeguard-20b, allam blocked at project level). Rate limit 8,000 tokens/min — the main bottleneck.
- Tavily: 8 grounding searches (CBN BVN warnings, fake alerts/POS, CBEX/EFCC, FCCPC loan apps, SIM swap, NIS/INEC fake recruitment, fake FG grant, romance scams) saved to `data/seeds/tavily_seeds.json`.
- Generation: 136 jobs (17 types × 5 languages, 12 msgs each) via `scripts/generate_dataset.py`, resumable, run in ~90 s chunks.
- After first chunk: tightened prompt (no channel prefixes, varied account masks, hard negatives must never ask for OTP/PIN/BVN or unknown links, stay in target language).
- Generation finished: 153 jobs → 1,834 raw rows (+36 hand-written seeds). Hit Groq free-tier **200k tokens/day** cap right after.
- `build_dataset.py`: 1,821 final rows (982 scam / 839 legit; en 747, pcm 465, yo 203, ig 199, ha 207). Splits 1,274 / 182 / 365.
- Baselines: rules 72.0% acc; TF-IDF+LogReg 97.8% acc / 97.8 macro-F1 (test). Trained in ~3 s.
- Sandbox restarted mid-run (pip packages lost, workspace kept) — reinstalled and continued.
- Fine-tuned Davlan/afro-xlmr-mini (frozen embeddings, 3 epochs, 6 resumable ~95 s chunks, 519 s total): 94.2% acc / 94.2 macro-F1. Weights kept local (466 MB, gitignored).
- Hand-written challenge set (40 msgs): TF-IDF 75.0%, afro-xlmr-mini 67.5%, rules 60.0%. Challenge scam recall: TF-IDF 10/20, xlmr 7/20, gpt-oss-120b 19/20.
- LLM zero-shot (gpt-oss-120b): only partial — 70/365 test (all happened to be scams; 70/70 correct) and 20/40 challenge before the daily quota ran out. Scripts are resumable.
- Other Groq models (gpt-oss-20b, qwen3.8-27b, safeguard, allam) are blocked at the Groq project level → second LLM not run.
- App: Gradio app tested locally (function calls + server launch + gradio_client API call). LLM explanation path worked once before the quota ran out; offline fallback verified.
- pytest: 9 passed. Space bundle verified via scripts/prepare_space.sh.
- GitHub: `repo_create` returned **403 "Resource not accessible by integration"** — the Hark GitHub integration cannot create repositories. Git over HTTPS works for repos it can access. Committed locally; ready to push once the empty private repo `shora` exists.
- 2026-10-08 23:30 WAT — Gradio Spaces now return **402 (HF PRO required)**, so built a free **static** Space instead.
  `scripts/export_static.py` exports the shipped TF-IDF+LogReg heads (shared vocab of 7,112 word + 24,722 char_wb
  features, integer df, int16 coefs per-class scale) and the 15 regex rules (Python→Unicode-aware JS) to
  `space-static/model.js` (1.87 MB; whole Space 1.9 MB). `space-static/shora.js` re-implements the pipeline in JS.
- Parity (`scripts/check_static_parity.py`, node 22): test set 365/365 = **100%** same binary label and scam type,
  100% same red flags and blended verdict, max |Δp| 3.2e-5. All 1,861 messages: also 100%.
- Published private static Space **Nihilitybot666/shora** (https://huggingface.co/spaces/Nihilitybot666/shora), RUNNING;
  checked in a real browser (example tap, Hausa advice). Advice is pre-written per scam type in EN/PCM/YO/IG/HA;
  scam-type names and rule-flag labels are still English only.
- Already on the Hub (private): dataset **Nihilitybot666/naijascam**, model **Nihilitybot666/shora-tfidf**.
