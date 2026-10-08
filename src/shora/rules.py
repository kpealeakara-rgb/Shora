"""Transparent, rule-based red-flag detector.

These rules never decide the verdict on their own; they surface *why* a message looks risky so the
explanation is grounded in the text. Works offline and in all five languages (keywords are mixed).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    key: str
    pattern: re.Pattern
    flag: str          # short English label
    weight: float      # contribution to the heuristic risk score


def _r(p: str) -> re.Pattern:
    return re.compile(p, re.I)


RULES: list[Rule] = [
    Rule("asks_secret", _r(r"(send|share|give|forward|read|reply|tell|drop|fi\s+.*ránṣẹ́|turo|tura|zitere|nye)\b.{0,40}"
                           r"\b(otp|pin|bvn|nin|password|token|puk|cvv|code|lambar)\b"),
         "Asks you to share an OTP, PIN, BVN or code", 3.0),
    Rule("short_link", _r(r"\b(bit\.ly|tinyurl|t\.ly|cutt\.ly|is\.gd|rb\.gy|shorturl|goo\.gl|tiny\.cc|wa\.me)/\S+"),
         "Uses a shortened or unofficial link", 1.5),
    Rule("odd_domain", _r(r"\b[\w-]+\.(xyz|top|online|info|site|click|live|blogspot\.com|ng\.com|com\.ng-\w+)\b"),
         "Link points to an unusual domain", 1.5),
    Rule("account_block", _r(r"(block|restrict|suspend|deactivat|freeze|barred|frozen|go block|don block|ti dí|a rufe|akwụsị)"),
         "Threatens to block or suspend your account/SIM", 1.5),
    Rule("urgency", _r(r"(urgent|immediately|within \d+ ?(hrs?|hours|minutes|mins)|today only|before \d|sharp sharp|now now|"
                       r"gaggawa|ngwa ngwa|kíákíá|last chance|expires? (today|soon))"),
         "Creates urgency or a deadline", 1.0),
    Rule("upfront_fee", _r(r"(processing|registration|activation|clearance|withdrawal|form|medical|waybill|delivery|unlock|tax)"
                           r"\s*(fee|charge|levy)"),
         "Asks for an upfront fee before you get money/goods", 2.0),
    Rule("high_returns", _r(r"(\d{1,3}\s?% (daily|weekly|per day|every day|kowace rana|lójoojúmọ́)|double your|guarantee[ds]? "
                            r"(profit|return)|no risk|risk[- ]free|ai (trading|arbitrage|robot)|arbitrage|quant)"),
         "Promises guaranteed or unrealistic returns", 2.5),
    Rule("free_money", _r(r"(grant|giveaway|free \S*\s?(n|₦|ngn)?[\d,]+|claim your|you (have )?won|congratulations|tallafi|"
                          r"empowerment fund)"),
         "Offers free money, a grant or a prize", 1.5),
    Rule("refund_overpay", _r(r"(overpa|mistakenly|wrong(ly)? (transfer|sent)|refund the (excess|balance)|reverse (the|my)|"
                              r"send (back|the balance))"),
         "Asks you to refund an 'overpayment' or 'wrong transfer'", 2.0),
    Rule("release_goods", _r(r"(pending|network (delay|issue)|release the (goods|item)|load the goods|it will reflect|go reflect)"),
         "Says payment is 'pending' and pushes you to release goods", 1.5),
    Rule("shame_threat", _r(r"(fraudster|thief|debtor|your contacts|all your contacts|post your (picture|photo)|disgrace|"
                            r"we (will|go) (come|tag|expose))"),
         "Threatens to shame you or contact your people", 2.0),
    Rule("job_fee", _r(r"(shortlisted|recruitment|visa sponsorship|cos\b|certificate of sponsorship|lmia|scholarship)"),
         "Job, visa or scholarship offer (check if it asks for money)", 0.8),
    Rule("customs_love", _r(r"(my love|darling|baby|sweetheart).{0,120}(customs|package|parcel|gift card|hospital|stuck)"),
         "Online partner asking for money for a package/emergency", 2.0),
    Rule("telco_pretext", _r(r"(sim (swap|upgrade|re-?registration)|5g sim|esim|puk|switch off your phone|dial \*\d+)"),
         "SIM upgrade/re-registration pretext (SIM-swap risk)", 2.0),
    Rule("personal_account", _r(r"(my (personal )?(account|opay|palmpay|moniepoint)|agent'?s account|to mr\.? \w+'?s account)"),
         "Payment to a personal account instead of an official one", 1.0),
]

SAFE_HINTS = [
    _r(r"(do not|don't|never)\s+(share|disclose|give)"),
    _r(r"avail(able)?\s*bal"),
]


def find_red_flags(text: str) -> list[dict]:
    out = []
    for rule in RULES:
        m = rule.pattern.search(text or "")
        if m:
            out.append({"key": rule.key, "flag": rule.flag, "evidence": m.group(0)[:60], "weight": rule.weight})
    return out


def heuristic_score(text: str) -> float:
    """0..1 risk score from rules only (used as a feature and as an offline fallback)."""
    s = sum(f["weight"] for f in find_red_flags(text))
    if any(p.search(text or "") for p in SAFE_HINTS):
        s -= 1.5
    return max(0.0, min(1.0, s / 5.0))
