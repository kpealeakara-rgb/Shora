"""Hand-written seed messages modelled on patterns described in public warnings.

Each seed is written by the Shora authors (not copied from a real victim) and points to the public source
whose described pattern it imitates. Columns: text, label, scam_type, language, red_flags, ref.
"""
CBN = "https://ru.scribd.com/document/352642175/CBN-Press-Statement-on-BVN"
FAKE_ALERT = "https://humanglemedia.com/fake-alerts-dubious-stunts-the-digital-scams-draining-nigerias-pos-economy"
CBEX = "https://www.france24.com/en/live-news/20250701-cbex-crypto-scam-ai-hyped-ponzi-scheme-defrauds-african-investors"
FCCPC = "https://nairacompare.ng/blogs/fccpcs-guide-to-protecting-your-rights-against-loan-app-harassment"
JOBS = "https://scamcheck.tech/scams/job-scam-nigeria"
GRANT = "https://haltfake.org/no-the-federal-government-is-not-giving-%E2%82%A6250000-grant"
PAGA = "https://technext24.com/news/paga-fraud-alert-over-whatsapp-giveaway"
ROMANCE = "https://en.wikipedia.org/wiki/Advance-fee_scam"

SEEDS = [
    # bank / BVN impersonation
    ("Dear Customer, your account has been restricted due to incomplete BVN linkage as directed by CBN. Update within 24hrs to avoid permanent deactivation: bvn-update-ng.com/verify", "scam", "bank_impersonation_otp", "en", ["threat of deactivation", "unofficial link", "24-hour deadline"], CBN),
    ("This is NIBSS customer care. Your BVN has been flagged for multiple accounts. To unflag, read the 6-digit code we just sent to your phone.", "scam", "bank_impersonation_otp", "en", ["asks for OTP", "caller claims NIBSS", "account flag threat"], CBN),
    ("Oga, na from your bank I dey call. Dem don block your ATM card because of NIN. Abeg send me the code wey dem go send you now make I unblock am.", "scam", "bank_impersonation_otp", "pcm", ["asks for code", "unsolicited bank call", "card block threat"], CBN),
    ("Àkáǹtì yín ti dí nítorí BVN. Ẹ tẹ link yìí láti ṣe update: bit.ly/bvn-ng24, kí ẹ sì fi OTP ránṣẹ́ sí wa.", "scam", "bank_impersonation_otp", "yo", ["short link", "asks for OTP", "account blocked claim"], CBN),
    ("Asusu gị ka akwụsịrị n'ihi NIN. Pịa link a ka i mezie ya taa: nimc-verify.info. Ọ bụrụ na i meghị, ego gị ga-efu.", "scam", "bank_impersonation_otp", "ig", ["fake NIMC link", "threat of loss", "same-day deadline"], CBN),
    ("An rufe asusun ka saboda BVN. Ka tura lambar OTP da muka aiko maka yanzu domin a bude shi.", "scam", "bank_impersonation_otp", "ha", ["asks for OTP", "account closed claim"], CBN),
    # fake credit alert
    ("I don send the N85,000 for the 2 bags of rice. Check am, na network delay. Abeg load the goods make my driver carry am sharp sharp.", "scam", "fake_credit_alert", "pcm", ["pressure to release goods", "blames network delay", "no confirmed credit"], FAKE_ALERT),
    ("Sorry I mistakenly transferred N50,000 instead of N5,000 to your POS. Please reverse the N45,000 balance to my Opay 81******02, God bless you.", "scam", "fake_credit_alert", "en", ["overpayment refund request", "mistaken transfer story", "refund to different account"], FAKE_ALERT),
    ("Credit Alert! Acct: 22****1093 Amt: NGN350,000.00 CR Desc: TRF FRM CHUKWU... Avail Bal: NGN350,412.55 — sent via WhatsApp, not from your bank.", "scam", "fake_credit_alert", "en", ["alert sent by buyer", "not from bank channel", "check bank app"], FAKE_ALERT),
    # ponzi
    ("CBEX-style AI arbitrage robot: deposit $100 earn 5% daily, refer 3 friends unlock VIP. Withdrawal open after you pay 10% tax. Registered with SEC (cert attached).", "scam", "ponzi_crypto", "en", ["guaranteed daily returns", "withdrawal fee", "referral levels", "fake SEC claim"], CBEX),
    ("Abeg join our AI trading group. Put N200k, in 30 days e go turn N1.2m. Na robot dey trade, no risk at all. Admin go add you for Telegram.", "scam", "ponzi_crypto", "pcm", ["unrealistic returns", "no risk claim", "Telegram group"], CBEX),
    ("Ẹ fi ₦50,000 sí platform AI trading wa, ẹ máa gba ₦5,000 lójoojúmọ́. Kò sí ewu rárá. Ẹ pe àwọn ọ̀rẹ́ yín láti gba bonus.", "scam", "ponzi_crypto", "yo", ["fixed daily profit", "no risk claim", "referral bonus"], CBEX),
    ("Saka ₦100,000 a shirin mu na AI trading, za ka samu riba 10% kowace rana. Ka kawo abokai biyar don karin bonus.", "scam", "ponzi_crypto", "ha", ["10% daily return", "recruit friends"], CBEX),
    # loan app
    ("You are a debtor and a thief. If you don't pay N38,500 today we will send your picture to all your contacts and tag you FRAUDSTER on Facebook.", "scam", "loan_app_extortion", "en", ["threat to shame contacts", "defamation threat", "same-day ultimatum"], FCCPC),
    ("Your friend Emeka don borrow money for our app put your number as guarantor. If e no pay by 5pm we go come your office. Pay am now.", "scam", "loan_app_extortion", "pcm", ["harassing third party", "physical threat", "illegal guarantor claim"], FCCPC),
    ("Loan of N500,000 approved instantly with no BVN check! Pay N7,500 processing fee to 70*****12 to receive disbursement in 5 minutes.", "scam", "loan_app_extortion", "en", ["upfront processing fee", "too-easy approval", "personal account"], FCCPC),
    # jobs
    ("Congratulations! You have been shortlisted for NNPC graduate trainee 2026. Pay N15,000 for medicals and form to Mr. Bello's account to confirm your slot.", "scam", "fake_job_visa_scholarship", "en", ["fee for job", "payment to individual", "no interview"], JOBS),
    ("Canada visa sponsorship job: farm workers needed, salary $3,500/month. Pay N450,000 for LMIA + Certificate of Sponsorship. Limited slots. WhatsApp only.", "scam", "fake_job_visa_scholarship", "en", ["pay for sponsorship", "WhatsApp only", "limited slots pressure"], JOBS),
    ("Immigration (NIS) recruitment portal don open! Apply for this link nis-recruit2026.com.ng, pay N3,000 form fee before Friday.", "scam", "fake_job_visa_scholarship", "pcm", ["unofficial portal", "application fee", "deadline pressure"], JOBS),
    # grants
    ("The Federal Government is giving N250,000 grant to every Nigerian to support businesses. Apply now before the portal closes: fg-grant-2026.blogspot.com", "scam", "giveaway_grant", "en", ["free money promise", "blogspot link", "portal closing pressure"], GRANT),
    ("Paga is celebrating 15 years! Claim your free N50,000 now, share to 10 WhatsApp groups to activate: paga-anniversary.xyz", "scam", "giveaway_grant", "en", ["share-to-claim", "fake anniversary", "unofficial domain"], PAGA),
    ("Gwamnatin tarayya na bayar da tallafin ₦250,000 ga matasa. Danna wannan link ka cike bayanan katin ATM dinka: tallafi-ng.online", "scam", "giveaway_grant", "ha", ["free grant", "asks card details", "unofficial link"], GRANT),
    ("Ọchịchị etiti na-enye ₦250,000 maka ndị ntorobịa. Kesaa ozi a n'otu iri wee pịa link: fg-empower.top", "scam", "giveaway_grant", "ig", ["free grant", "share to 10 groups", "suspicious domain"], GRANT),
    # romance
    ("My love, I am a US soldier in Syria. I sent you a box with $850,000 and gold but customs at Lagos airport need N380,000 clearance. Please pay to the agent today.", "scam", "romance_yahoo", "en", ["online lover asks money", "customs fee for package", "foreign soldier story"], ROMANCE),
    # sim swap
    ("MTN: Your SIM will be barred in 2hrs due to NIN mismatch. Call our agent on 0907******1 and give him the PUK code to upgrade to 5G SIM.", "scam", "sim_swap", "en", ["asks for PUK", "barring threat", "agent phone number"], CBN),
    # legit
    ("Acct:01******89\nAmt:NGN5,000.00 DR\nDesc:NIP/TRF TO ADEBAYO T\nDate:08-Oct-26 14:22\nAvail Bal:NGN43,210.50", "legit", "legit_bank_alert", "en", [], ""),
    ("Your OTP for transfer of NGN20,000.00 is 482915. It expires in 5 minutes. Do not disclose this code to anyone, including bank staff.", "legit", "legit_otp", "en", [], ""),
    ("Reminder: we will NEVER call you to ask for your BVN, PIN, OTP or card details. If anyone does, end the call and report via our official app.", "legit", "legit_security_advisory", "en", [], CBN),
    ("Mama, I don reach hostel o. Light no dey but I dey fine. I go call you after lecture tomorrow. Greet Papa for me.", "legit", "legit_family_chat", "pcm", [], ""),
    ("Payment received: RRR 3110-4498-2271 for School Fees 2026/2027, amount NGN64,500.00. Print your receipt from the school portal.", "legit", "legit_school_remita", "en", [], ""),
    ("Your Jumia order 3398210 has been shipped and will be delivered between Fri 10 and Mon 13 Oct. Pay on delivery or track in the app.", "legit", "legit_delivery", "en", [], ""),
    ("Ẹ káàrọ̀ Màmá, ṣé ara yín le? A máa wá sí ilé ní Sunday lẹ́yìn ìsìn. Ẹ kí Bàbá fún wa.", "legit", "legit_family_chat", "yo", [], ""),
    ("Nne, ezigbo ụtụtụ. Ana m abịa ụlọ Saturday. Kedu ka ahụ gị dị?", "legit", "legit_family_chat", "ig", [], ""),
    ("Salam Baba, mun isa Kano lafiya. Za mu gaishe ku gobe in Allah ya yarda.", "legit", "legit_family_chat", "ha", [], ""),
    ("Dear subscriber, you have successfully recharged N1,000. Your new balance is N1,045.60. Dial *310# to check balance.", "legit", "legit_telco_utility", "en", [], ""),
    ("Customer, your hair don ready. Balance na N3,000, you fit pay when you come pick am. Thank you for patronising Joy Salon.", "legit", "legit_business_vendor", "pcm", [], ""),
]
