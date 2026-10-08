"""Minimal Groq (OpenAI-compatible) client with rate-limit aware retries.

Only the standard library + requests. Set GROQ_API_KEY in the environment.
"""
from __future__ import annotations

import json
import os
import re
import time

import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("SHORA_LLM_MODEL", "openai/gpt-oss-120b")


class LLMError(RuntimeError):
    pass


def _parse_wait(resp: requests.Response) -> float:
    for h in ("retry-after", "x-ratelimit-reset-tokens"):
        v = resp.headers.get(h)
        if not v:
            continue
        try:
            return float(v)
        except ValueError:
            m = re.match(r"(?:(\d+)m)?([\d.]+)s", v)
            if m:
                return int(m.group(1) or 0) * 60 + float(m.group(2))
    return 5.0


def chat(messages, model: str = DEFAULT_MODEL, json_mode: bool = True, temperature: float = 0.9,
         max_tokens: int = 2500, retries: int = 6, timeout: int = 90, deadline: float | None = None,
         **extra) -> str:
    key = os.environ.get("GROQ_API_KEY", "")
    payload = {"model": model, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    if "gpt-oss" in model:
        payload["reasoning_effort"] = extra.pop("reasoning_effort", "low")
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    payload.update(extra)
    last = None
    for _ in range(retries):
        if deadline and time.time() > deadline:
            break
        try:
            r = requests.post(GROQ_URL, json=payload, timeout=timeout,
                              headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        except requests.RequestException as e:  # network blip
            last = str(e)
            time.sleep(3)
            continue
        if r.status_code == 429:
            wait = _parse_wait(r)
            if wait > 60 or r.headers.get("x-should-retry") == "false":  # daily quota: fail fast
                raise LLMError(f"rate limited (retry in {wait:.0f}s): {r.text[:160]}")
            time.sleep(wait + 0.5)
            last = "rate limited"
            continue
        if r.status_code >= 500:
            last = f"server {r.status_code}"
            time.sleep(3)
            continue
        if r.status_code != 200:
            raise LLMError(f"{r.status_code}: {r.text[:300]}")
        return r.json()["choices"][0]["message"]["content"]
    raise LLMError(f"gave up: {last}")


def chat_json(messages, **kw) -> dict:
    txt = chat(messages, json_mode=True, **kw)
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", txt, re.S)
        if not m:
            raise LLMError("no JSON in response")
        return json.loads(m.group(0))
