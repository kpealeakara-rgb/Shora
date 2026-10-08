"""NaijaScam taxonomy: scam types, legit message types and languages."""
from __future__ import annotations

LANGUAGES = {
    "en": "English (Nigerian English)",
    "pcm": "Nigerian Pidgin",
    "yo": "Yoruba",
    "ig": "Igbo",
    "ha": "Hausa",
}

# scam_type -> (short name, description used for generation + explanations, public grounding)
SCAM_TYPES = {
    "fake_credit_alert": (
        "Fake credit alert",
        "Fake bank credit alerts or edited transfer screenshots sent to traders, POS agents and online vendors; "
        "overpayment then 'please refund the excess'; 'transfer pending, release the goods'; reversal fraud.",
        "Humangle, mytreda.com, trustbillmarket.com warnings on POS/vendor fake alerts",
    ),
    "bank_impersonation_otp": (
        "Bank / BVN / NIN impersonation & OTP theft",
        "Messages pretending to be a bank, CBN, NIBSS or NIMC saying the BVN/NIN/account is blocked, restricted or "
        "must be 'updated/linked' via a link or phone call; asks for OTP, PIN, card details or token code.",
        "CBN press statements on fraudulent BVN messages (2017, Apr 2026); bank customer alerts",
    ),
    "sim_swap": (
        "SIM-swap pretext",
        "Fake telco (MTN, Airtel, Glo, 9mobile) or NCC messages: SIM must be re-registered, upgraded to 5G/eSIM, "
        "NIN-SIM linkage failed; asks to dial a code, share a PIN/PUK or OTP, or to switch off the phone.",
        "Bank/NCC SIM-swap and OTP-interception warnings",
    ),
    "ponzi_crypto": (
        "Ponzi / crypto 'AI trading' investment",
        "CBEX-style 'AI arbitrage/quant trading' platforms promising fixed daily returns (e.g. 5-100%), referral "
        "bonuses, 'withdrawal fee to unlock profit', fake SEC/EFCC certificates, Telegram/WhatsApp signal groups.",
        "EFCC labelled CBEX a Ponzi (France24, Al Jazeera 2025); SEC Nigeria Ponzi warnings",
    ),
    "loan_app_extortion": (
        "Loan-app harassment / extortion",
        "Illegal digital lenders threatening to tell contacts, post defamatory 'fraudster' broadcasts, edit photos, "
        "demand rollover fees, or 'instant loan approved, pay processing fee first'.",
        "FCCPC loan-app harassment guidance; DEON Consumer Lending Regulation (Jul 2025)",
    ),
    "fake_job_visa_scholarship": (
        "Fake job / visa / scholarship",
        "Fake recruitment (NIS, NNPC, banks, INEC), Canada/UK visa-sponsorship jobs, fully funded scholarships; "
        "asks for form/medical/processing/CoS fee paid to a personal account; Gmail recruiter; pay-to-like tasks.",
        "Nigeria Immigration Service & INEC fake-recruitment warnings (2024-2026); scamcheck.tech",
    ),
    "romance_yahoo": (
        "Romance / 'yahoo' scam",
        "Online lover, foreign soldier/oil-rig engineer, 'package stuck at customs, pay clearance', gift card asks, "
        "sudden emergency hospital bill, sextortion threats.",
        "Advance-fee/romance scam reporting (ISS Africa ENACT, NPR 2026)",
    ),
    "fake_vendor_pos": (
        "Fake vendor / marketplace / POS",
        "Instagram/WhatsApp/Jiji vendors demanding full payment upfront for cheap phones, cars, rent or 'tokunbo' items, "
        "fake delivery agents demanding 'waybill fee', fake rental agents, POS 'reverse my wrong transfer' tricks.",
        "Consumer warnings on online vendor and reversal fraud",
    ),
    "giveaway_grant": (
        "Giveaway / fake government grant",
        "Fake FG/CBN/NYIF grants (e.g. ₦250,000), Tinubu/Dangote/MTN/bank anniversary giveaways, 'click to claim ₦50,000', "
        "requires forwarding to 10 groups, paying a 'registration/activation fee' or entering card details.",
        "haltfake.org on fake ₦250,000 FG grant; Africa Check; Paga ₦50,000 WhatsApp giveaway alert",
    ),
}

LEGIT_TYPES = {
    "legit_bank_alert": (
        "Genuine bank debit/credit alert",
        "Real-format debit/credit transaction alerts from GTBank, Access, Zenith, UBA, First Bank, OPay, Moniepoint, "
        "Palmpay, Kuda: masked account, amount, description, date, available balance. No links, no requests.",
    ),
    "legit_otp": (
        "Genuine OTP / verification code",
        "Genuine one-time codes for transfers, logins, Jumia, Bolt, WhatsApp, banks; always say 'do not share this code'.",
    ),
    "legit_delivery": (
        "Genuine delivery / ride / order update",
        "Jumia, Konga, GIG Logistics, DHL, Glovo, Chowdeck, Bolt/Uber updates with order numbers; no payment requests "
        "outside the app.",
    ),
    "legit_school_remita": (
        "School / Remita / exam notice",
        "University, JAMB, WAEC, NYSC notices; Remita RRR payment confirmations; course registration deadlines; "
        "lecturer and class-rep messages.",
    ),
    "legit_family_chat": (
        "Family / friends chat",
        "Everyday WhatsApp chats between family and friends: greetings, church/mosque, owambe plans, asking after health, "
        "normal requests to send small money between people who clearly know each other.",
    ),
    "legit_security_advisory": (
        "Genuine bank / agency security advisory",
        "Real awareness messages from banks/CBN/EFCC/NCC: 'we will never ask for your PIN/OTP', report fraud via official "
        "channels. Mentions scams but is NOT a scam (hard negative).",
    ),
    "legit_business_vendor": (
        "Genuine business / vendor / service",
        "Real customer-service and small-business messages: tailor, hairdresser, mechanic, landlord, POS agent, "
        "invoice after delivery, appointment reminders, receipts.",
    ),
    "legit_telco_utility": (
        "Genuine telco / utility / subscription",
        "MTN/Airtel/Glo data balance, recharge confirmation, DStv/GOtv renewal, electricity token (IKEDC, EKEDC, AEDC), "
        "LAWMA bill reminders.",
    ),
}

ALL_TYPES = {**{k: v[:2] for k, v in SCAM_TYPES.items()}, **{k: v[:2] for k, v in LEGIT_TYPES.items()}}


def is_scam_type(t: str) -> bool:
    return t in SCAM_TYPES
