#!/usr/bin/env bash
# Build a flat, self-contained Hugging Face Space folder in ./space
# Usage: bash scripts/prepare_space.sh && cd space && git init && ... (or: huggingface-cli upload <user>/shora space --repo-type space)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/space"
rm -rf "$OUT" && mkdir -p "$OUT/src" "$OUT/models"
cp "$ROOT/app/app.py" "$ROOT/app/requirements.txt" "$ROOT/app/README.md" "$OUT/"
cp -r "$ROOT/src/shora" "$OUT/src/"
cp -r "$ROOT/models/tfidf-logreg" "$OUT/models/"
find "$OUT" -name "__pycache__" -prune -exec rm -rf {} +
echo "Space ready in $OUT ($(du -sh "$OUT" | cut -f1))"
