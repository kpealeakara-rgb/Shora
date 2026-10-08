"""NaijaScam-Challenge v0.1: 40 hand-written messages in a different style from the generator.

Purpose: an out-of-distribution sanity check. The main test split comes from the same generator as
train, so it over-estimates real-world accuracy; this set is written by hand, short, messy and tricky.
Run: python data/challenge/make_challenge.py -> data/naijascam/challenge.jsonl
"""
import json
from pathlib import Path

S, L = "scam", "legit"
ROWS = [
    # --- scams (20) ---
    ("Hello dear its me your pastor, I am in a meeting. Kindly help me buy 2 MTN N10k recharge cards and send the pins here urgently, will refund", S, "giveaway_grant", "en"),
    ("This is Bolt support. Your driver account has a pending payout of N63,200. Confirm the 6 digit number we sent you so we can release it", S, "bank_impersonation_otp", "en"),
    ("Bros I see your number for Jiji. The iPhone 13 still dey? I don pay N420k, check the screenshot. My boy go pick am now now", S, "fake_credit_alert", "pcm"),
    ("Na me Uche from church. My mama dey hospital, abeg send 15k to this Palmpay 9047******3 na my cousin own, my own account get issue", S, "romance_yahoo", "pcm"),
    ("Your NIN-SIM linkage is incomplete. Reply YES and you will receive a call from our NCC officer to complete it. Do not switch off your phone", S, "sim_swap", "en"),
    ("Good evening sir. You were selected for Shell Petroleum internship 2026, stipend N350,000/month. Training kit costs N25,000 payable to the HR coordinator", S, "fake_job_visa_scholarship", "en"),
    ("Investment wey dey pay 30% every Friday. My cousin don collect 3 times. Minimum na 50k. Na the last slot be this", S, "ponzi_crypto", "pcm"),
    ("DEBT NOTICE: Akara has refused to pay N12,400 to QuickNaira. If you know him tell him to pay or his NIN will be blacklisted by EFCC", S, "loan_app_extortion", "en"),
    ("Your Konga parcel could not be delivered due to incomplete address. Pay N1,050 redelivery fee here: konga-redeliver.top", S, "fake_vendor_pos", "en"),
    ("Mo ti ṣàṣìṣe fi ₦30,000 ránṣẹ́ sí account yín dípò ₦3,000. Ẹ jọ̀ọ́ ẹ dá ₦27,000 padà sí OPay mi", S, "fake_credit_alert", "yo"),
    ("Banki yín ni a ti ń pè. A fẹ́ dí card yín. Ẹ ka nọ́mbà tí ẹ ṣẹ̀ṣẹ̀ gbà fún wa kí a lè dá a dúró", S, "bank_impersonation_otp", "yo"),
    ("Ndewo! I meriri ₦500,000 na mmemme Dangote Foundation. Kwụọ ₦4,500 maka nnyefe ka anyị zitere gị ego ahụ", S, "giveaway_grant", "ig"),
    ("Nwanne, tinye ₦100k na crypto bot a, ọ na-enye 15% kwa ụbọchị. Enweghị ihe egwu ọ bụla", S, "ponzi_crypto", "ig"),
    ("Assalamu alaikum. An zabe ka don aikin Hukumar Kwastam. Ka biya ₦20,000 kudin fom zuwa wannan asusun kafin Juma'a", S, "fake_job_visa_scholarship", "ha"),
    ("Masoyiyata, kayan da na aiko miki suna kwastam a Abuja. Ki biya $300 domin a sake su yau", S, "romance_yahoo", "ha"),
    ("URGENT: Your Moniepoint POS terminal will be deactivated tonight. Call our agent 0815******4 to re-profile with your card PIN", S, "bank_impersonation_otp", "en"),
    ("Thank you for registering for the CBN Covid relief fund. Your N150,000 is ready. Enter your ATM card details on the portal to receive", S, "giveaway_grant", "en"),
    ("Abeg no vex, I wrongly sent you airtime of 5k from my line. Kindly transfer the 5k back to my GTB", S, "fake_credit_alert", "pcm"),
    ("Earn N2,000 per task by liking TikTok videos. Join our Telegram, pay N7,500 to activate your VIP task account", S, "fake_job_visa_scholarship", "en"),
    ("If you no pay by 6pm we go post your picture for your WhatsApp contacts say you be thief. Last warning", S, "loan_app_extortion", "pcm"),
    # --- legit (20) ---
    ("Your transfer of N15,000.00 to CHIOMA OKAFOR was successful. Ref: 000013261008. Thank you for banking with us.", L, "legit_bank_alert", "en"),
    ("Your one-time password is 552901. Valid for 10 mins. If you did not request this, call 0700-XXX-XXXX. Never share this code.", L, "legit_otp", "en"),
    ("Pls when you reach house send me the 2k for the bread wey I buy for you this morning", L, "legit_family_chat", "pcm"),
    ("Class rep: CSC 201 test has been moved to Thursday 10am at LT2. Bring your ID card.", L, "legit_school_remita", "en"),
    ("Hi Akara, your Chowdeck order from Item 7 is on the way. Rider: Musa. ETA 25 mins.", L, "legit_delivery", "en"),
    ("Fraud alert from your bank: we will never ask you to transfer money to a 'safe account'. Stay vigilant.", L, "legit_security_advisory", "en"),
    ("Oga I don finish the AC repair. Na 18k total, you fit send am to my account when you check say e dey cool well.", L, "legit_business_vendor", "pcm"),
    ("You have been gifted 1.5GB data by 0803***5512. Valid for 7 days. Dial *323# to check.", L, "legit_telco_utility", "en"),
    ("Ẹ̀gbọ́n mi, ẹ kú iṣẹ́ o. A ó pàdé ní ọjà Bodija lọ́la ní aago mẹ́wàá.", L, "legit_family_chat", "yo"),
    ("Ẹ jọ̀ọ́ ẹ rán aṣọ ìyàwó mi wá ní Sátidé. Mo ti san owó tó kù tán.", L, "legit_business_vendor", "yo"),
    ("Nne m, anyị ga-agba ụka n'elekere asatọ echi. Biko kwadebe ụmụaka.", L, "legit_family_chat", "ig"),
    ("Ụgwọ ọkụ gị: Token 4512-8890-1123-0076-3321, 45.2kWh. Daalụ maka iji EEDC.", L, "legit_telco_utility", "ig"),
    ("Baba, mun aika maka kudin makaranta na Aisha ₦45,000. Ka duba ka gani ya shiga.", L, "legit_family_chat", "ha"),
    ("An tura kayanka daga Kano. Lambar bin diddigi: GIG-88231. Za ka karba gobe.", L, "legit_delivery", "ha"),
    ("Dear student, your 2026/2027 school fees payment (RRR 2901-3381-1173) of N58,250 has been confirmed. Proceed to course registration on the portal.", L, "legit_school_remita", "en"),
    ("Your DStv Compact subscription has been renewed. Next due date: 08/11/2026. Thank you.", L, "legit_telco_utility", "en"),
    ("Mama Tobi, the soup don ready o. Make you send Tobi come carry am before 7.", L, "legit_family_chat", "pcm"),
    ("Reminder: your appointment at Reddington Hospital is tomorrow 9:30am. Reply 1 to confirm or call the front desk to reschedule.", L, "legit_business_vendor", "en"),
    ("Debit Alert: Acct ***2210 Amt NGN2,500.00 Desc POS PURCHASE SHOPRITE IKEJA Bal NGN61,004.20", L, "legit_bank_alert", "en"),
    ("EFCC: Report fraud and scams through our official channels only. We do not charge any fee to recover your money.", L, "legit_security_advisory", "en"),
]


def main():
    out = Path(__file__).resolve().parents[1] / "naijascam" / "challenge.jsonl"
    with open(out, "w") as fh:
        for i, (t, lab, ty, lang) in enumerate(ROWS):
            fh.write(json.dumps({"id": f"ch-{i:03d}", "text": t, "label": lab, "scam_type": ty, "language": lang,
                                 "red_flags": [], "source": "seed", "generator": "hand-written"},
                                ensure_ascii=False) + "\n")
    print(len(ROWS), "->", out)


if __name__ == "__main__":
    main()
