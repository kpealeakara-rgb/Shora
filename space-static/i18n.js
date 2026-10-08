/* Pre-written UI text and safety advice in English, Naija Pidgin, Yorùbá, Igbo and Hausa. */
var SHORA_I18N = {
  langs: [["en", "English"], ["pcm", "Pidgin"], ["yo", "Yorùbá"], ["ig", "Igbo"], ["ha", "Hausa"]],

  ui: {
    en: { tagline: "Paste a suspicious SMS, WhatsApp message or email. Shora checks it for Nigerian scam patterns.",
          placeholder: "Paste the message here…", check: "Check message", clear: "Clear", examples: "Try an example",
          scamProb: "scam probability", type: "Likely pattern", flags: "Red flags found", noFlags: "No strong red flags found.",
          todo: "What to do", privacy: "Runs fully on your device. Nothing you paste leaves your phone.",
          never: "Never paste your PIN, OTP or password anywhere, including here.", loading: "Loading model…",
          empty: "Paste a message first.", careful: "The model leans safe, but the rules found warning signs. Be careful.",
          disclaimer: "Shora can be wrong. Always confirm with your bank's official number.", lang: "Language" },
    pcm: { tagline: "Paste any SMS, WhatsApp or email wey you no trust. Shora go check am for Naija scam style.",
          placeholder: "Paste the message for here…", check: "Check am", clear: "Clear", examples: "Try one example",
          scamProb: "chance say na scam", type: "Wetin e resemble", flags: "Red flags wey we see", noFlags: "We no see strong red flag.",
          todo: "Wetin you go do", privacy: "E dey run for your phone. Nothing wey you paste dey commot your phone.",
          never: "No ever paste your PIN, OTP or password anywhere, even here.", loading: "Model dey load…",
          empty: "Paste message first.", careful: "Model think say e safe, but the rules see some warning sign. Shine your eye.",
          disclaimer: "Shora fit make mistake. Always confirm with your bank official number.", lang: "Language" },
    yo: { tagline: "Ẹ lẹ SMS, ìfiránṣẹ́ WhatsApp tàbí email tí ẹ kò fọkàn tán síbí. Shora máa yẹ̀ ẹ́ wò fún ọgbọ́n jìbìtì.",
          placeholder: "Ẹ lẹ ìfiránṣẹ́ náà síbí…", check: "Yẹ̀ ẹ́ wò", clear: "Pa á rẹ́", examples: "Ẹ gbìyànjú àpẹẹrẹ kan",
          scamProb: "àǹfààní pé jìbìtì ni", type: "Ohun tó jọ", flags: "Àwọn àmì ewu", noFlags: "A kò rí àmì ewu tó lágbára.",
          todo: "Ohun tí ẹ máa ṣe", privacy: "Ó ń ṣiṣẹ́ lórí fóònù yín nìkan. Ohunkóhun tí ẹ lẹ̀ kò kúrò lórí fóònù yín.",
          never: "Ẹ má ṣe lẹ PIN, OTP tàbí password yín síbìkan, títí kan ibí.", loading: "A ń gbé model wọlé…",
          empty: "Ẹ kọ́kọ́ lẹ ìfiránṣẹ́ kan.", careful: "Model rò pé kò léwu, ṣùgbọ́n àwọn òfin rí àmì ìkìlọ̀. Ẹ ṣọ́ra.",
          disclaimer: "Shora lè ṣàṣìṣe. Ẹ máa fìdí rẹ̀ múlẹ̀ pẹ̀lú nọ́mbà banki yín.", lang: "Èdè" },
    ig: { tagline: "Tinye SMS, ozi WhatsApp ma ọ bụ email ị na-enyo enyo. Shora ga-enyocha ya maka ụzọ aghụghọ ndị Naịjirịa.",
          placeholder: "Tinye ozi ahụ ebe a…", check: "Nyochaa ozi", clear: "Hichapụ", examples: "Nwalee otu ihe atụ",
          scamProb: "ohere na ọ bụ aghụghọ", type: "Ụdị o yiri", flags: "Ihe ịdọ aka ná ntị", noFlags: "Ahụghị ihe ịdọ aka ná ntị siri ike.",
          todo: "Ihe ị ga-eme", privacy: "Ọ na-arụ ọrụ naanị na ekwentị gị. Ihe ọ bụla i tinyere anaghị apụ na ekwentị gị.",
          never: "Etinyela PIN, OTP ma ọ bụ password gị ebe ọ bụla, gụnyere ebe a.", loading: "A na-ebudata model…",
          empty: "Buru ụzọ tinye ozi.", careful: "Model chere na ọ dị mma, mana iwu ndị ahụ hụrụ ihe ịdọ aka ná ntị. Kpachara anya.",
          disclaimer: "Shora nwere ike imehie. Kwado ya mgbe niile na nọmba ụlọ akụ gị.", lang: "Asụsụ" },
    ha: { tagline: "Liƙa SMS, saƙon WhatsApp ko email da kake shakka. Shora zai duba shi don salon zamba na Najeriya.",
          placeholder: "Liƙa saƙon a nan…", check: "Duba saƙo", clear: "Goge", examples: "Gwada misali",
          scamProb: "yiwuwar zamba ne", type: "Irin salon", flags: "Alamun haɗari", noFlags: "Ba a ga alamun haɗari masu ƙarfi ba.",
          todo: "Abin da za ka yi", privacy: "Yana aiki a wayarka kaɗai. Babu abin da ka liƙa da ke barin wayarka.",
          never: "Kada ka taɓa liƙa PIN, OTP ko password ɗinka a ko'ina, har da nan.", loading: "Ana loda model…",
          empty: "Fara liƙa saƙo tukuna.", careful: "Model yana ganin babu matsala, amma dokoki sun ga alamun gargaɗi. Ka yi hankali.",
          disclaimer: "Shora na iya yin kuskure. Koyaushe ka tabbatar da lambar bankinka ta hukuma.", lang: "Harshe" }
  },

  verdict: {
    en: { scam: "Likely SCAM", legit: "Looks safe" },
    pcm: { scam: "E be like SCAM", legit: "E be like say e safe" },
    yo: { scam: "Ó dàbí JÌBÌTÌ (scam)", legit: "Ó dàbí pé kò léwu" },
    ig: { scam: "Ọ dị ka AGHỤGHỌ (scam)", legit: "Ọ dị ka ọ dị mma" },
    ha: { scam: "Da alama ZAMBA ce (scam)", legit: "Da alama babu matsala" }
  },

  types: {
    fake_credit_alert: ["💸", "Fake credit alert / overpayment"],
    bank_impersonation_otp: ["🏦", "Bank / BVN / NIN impersonation & OTP theft"],
    sim_swap: ["📶", "SIM-swap pretext"],
    ponzi_crypto: ["📈", "Ponzi / crypto 'AI trading'"],
    loan_app_extortion: ["📱", "Loan-app harassment / extortion"],
    fake_job_visa_scholarship: ["💼", "Fake job / visa / scholarship"],
    romance_yahoo: ["💔", "Romance / 'yahoo' scam"],
    fake_vendor_pos: ["🛒", "Fake vendor / delivery / POS"],
    giveaway_grant: ["🎁", "Giveaway / fake government grant"],
    legit_bank_alert: ["✅", "Genuine bank alert"],
    legit_otp: ["✅", "Genuine OTP / verification code"],
    legit_delivery: ["✅", "Genuine delivery / ride / order update"],
    legit_school_remita: ["✅", "School / Remita / exam notice"],
    legit_family_chat: ["✅", "Family / friends chat"],
    legit_security_advisory: ["✅", "Genuine security advisory"],
    legit_business_vendor: ["✅", "Genuine business / vendor message"],
    legit_telco_utility: ["✅", "Genuine telco / utility message"]
  },

  advice: {
    fake_credit_alert: {
      en: "Never trust an alert or a screenshot. Open your own bank app and check your real balance before you release goods or refund any 'excess'. Wrong transfers are reversed by the bank, not by you.",
      pcm: "No trust alert or screenshot. Open your own bank app check your real balance before you release goods or refund any 'excess'. If person send money by mistake, na bank go reverse am, no be you.",
      yo: "Ẹ má gbára lé alert tàbí screenshot. Ẹ ṣí app banki yín fúnra yín láti rí iye owó tó wọlé gan-an kí ẹ tó tú ẹrù sílẹ̀ tàbí dá owó 'àṣejù' padà. Banki ló ń dá owó tí wọ́n fi ránṣẹ́ ní àṣìṣe padà, kì í ṣe ẹ̀yin.",
      ig: "Atụkwasịla alert ma ọ bụ screenshot obi. Mepee app ụlọ akụ gị lelee ezigbo balance gị tupu i nyefee ngwa ahịa ma ọ bụ weghachi ego 'karịrị'. Ọ bụ ụlọ akụ na-eweghachi ego e zigara na mmejọ, ọ bụghị gị.",
      ha: "Kada ka amince da alert ko screenshot. Buɗe manhajar bankinka ka duba ainihin balance ɗinka kafin ka saki kaya ko ka mayar da wani kuɗin 'da ya wuce kima'. Banki ne ke mayar da kuɗin da aka tura bisa kuskure, ba kai ba."
    },
    bank_impersonation_otp: {
      en: "Your bank, CBN or NIMC will never ask for your OTP, PIN, BVN or password by SMS, call or link. Don't click or reply. Call the number on the back of your card or visit a branch.",
      pcm: "Your bank, CBN or NIMC no go ever ask for your OTP, PIN, BVN or password for SMS, call or link. No click, no reply. Call the number wey dey back of your card or waka go branch.",
      yo: "Banki yín, CBN tàbí NIMC kò ní béèrè OTP, PIN, BVN tàbí password yín láé lórí SMS, ìpè tàbí link. Ẹ má tẹ link, ẹ má sì fèsì. Ẹ pe nọ́mbà tó wà lẹ́yìn káàdì yín tàbí kí ẹ lọ sí ẹ̀ka banki.",
      ig: "Ụlọ akụ gị, CBN ma ọ bụ NIMC agaghị arịọ OTP, PIN, BVN ma ọ bụ password gị site na SMS, oku ma ọ bụ link. Apịala, azakwala. Kpọọ nọmba dị n'azụ kaadị gị ma ọ bụ gaa n'alaka ụlọ akụ.",
      ha: "Bankinka, CBN ko NIMC ba za su taɓa neman OTP, PIN, BVN ko password ɗinka ta SMS, kira ko link ba. Kada ka danna ko ka amsa. Kira lambar da ke bayan katinka ko ka je reshen banki."
    },
    sim_swap: {
      en: "Never share your PUK, PIN or any code, and never dial codes a stranger sends. Networks only upgrade SIMs at their own offices. If your line suddenly loses signal, call your bank to freeze your account.",
      pcm: "No ever give anybody your PUK, PIN or any code, and no dial code wey stranger send. Network dey upgrade SIM only for their own office. If your line just lose network sudden, call your bank make dem freeze your account.",
      yo: "Ẹ má fún ẹnikẹ́ni ní PUK, PIN tàbí kóòdù kankan, ẹ má sì tẹ kóòdù tí àjèjì fi ránṣẹ́. Ọ́fíìsì network nìkan ni wọ́n ti ń ṣe àtúnṣe SIM. Tí layin yín bá dédé pàdánù network, ẹ pe banki yín kí wọ́n dí àkáǹtì yín.",
      ig: "Enyela onye ọ bụla PUK, PIN ma ọ bụ koodu ọ bụla, akpọkwala koodu onye ị na-amaghị zitere. Network na-emezi SIM naanị n'ọfịs ha. Ọ bụrụ na SIM gị atụfuo network na mberede, kpọọ ụlọ akụ gị ka ha kpọchie akaụntụ gị.",
      ha: "Kada ka ba kowa PUK, PIN ko wata lamba, kuma kada ka danna lambar da baƙo ya turo maka. Kamfanin layi yana sabunta SIM ne a ofishinsa kaɗai. Idan layinka ya rasa network ba zato, kira bankinka su rufe asusunka."
    },
    ponzi_crypto: {
      en: "Guaranteed daily profit is the signature of a Ponzi scheme (remember CBEX). Don't deposit more and don't pay a 'withdrawal fee'. Check the company on the SEC Nigeria website and report it to the EFCC.",
      pcm: "Any platform wey promise sure profit every day na Ponzi (remember CBEX). No put more money and no pay any 'withdrawal fee'. Check the company for SEC Nigeria website and report am give EFCC.",
      yo: "Èrè ojoojúmọ́ tí wọ́n ṣèlérí láìsí ewu ni àmì Ponzi (ẹ rántí CBEX). Ẹ má fi owó kún un, ẹ má sì san 'withdrawal fee'. Ẹ yẹ ilé-iṣẹ́ náà wò lórí ìkànnì SEC Nigeria, kí ẹ sì fi tó EFCC létí.",
      ig: "Uru a kwere nkwa kwa ụbọchị bụ akara Ponzi (cheta CBEX). Etinyela ego ọzọ, akwụkwala 'withdrawal fee'. Lelee ụlọ ọrụ ahụ na weebụsaịtị SEC Nigeria ma kọọrọ EFCC.",
      ha: "Alƙawarin riba kowace rana ba tare da haɗari ba alamar Ponzi ce (ka tuna CBEX). Kada ka ƙara saka kuɗi, kuma kada ka biya 'kuɗin cirewa'. Duba kamfanin a shafin SEC Nigeria kuma ka kai rahoto ga EFCC."
    },
    loan_app_extortion: {
      en: "Don't pay 'processing fees' up front and don't give in to threats. Screenshot the messages, report the app to the FCCPC, and warn your close contacts that a loan app may send them lies about you.",
      pcm: "No pay any 'processing fee' before loan, and no let their threat fear you. Screenshot the messages, report the app give FCCPC, and tell your close people say loan app fit send dem lie about you.",
      yo: "Ẹ má san 'processing fee' ṣáájú, ẹ má sì jẹ́ kí ìhalẹ̀ dẹ́rù bà yín. Ẹ ya screenshot àwọn ìfiránṣẹ́ náà, ẹ fi app náà sùn FCCPC, kí ẹ sì kìlọ̀ fún àwọn èèyàn yín pé app awin lè fi irọ́ nípa yín ránṣẹ́ sí wọn.",
      ig: "Akwụla 'processing fee' tupu e nye gị mbinye ego, ekwekwala ka iyi egwu ha tụọ gị ụjọ. See screenshot ozi ndị ahụ, kọọ app ahụ n'FCCPC, ma gwa ndị gị na app mbinye ego nwere ike iziga ha ụgha maka gị.",
      ha: "Kada ka biya 'kuɗin sarrafawa' tun kafin a ba ka bashi, kuma kada barazana ta tsoratar da kai. Ɗauki screenshot na saƙonnin, ka kai rahoton manhajar ga FCCPC, kuma ka gargaɗi makusantanka cewa manhajar bashi na iya tura musu ƙarya game da kai."
    },
    fake_job_visa_scholarship: {
      en: "Real employers, embassies and scholarship boards don't ask you to pay form, medical or 'CoS' fees into a personal account. Check their official website yourself, and never pay to get a job.",
      pcm: "Real company, embassy or scholarship no dey ask you to pay form, medical or 'CoS' fee enter person account. Check their official website by yourself, and no ever pay money to get work.",
      yo: "Àwọn agbanisíṣẹ́ gidi, embassy àti àwọn tó ń fúnni ní scholarship kì í ní kí ẹ san owó fọ́ọ̀mù, medical tàbí 'CoS' sí àkáǹtì ẹnìkan. Ẹ fúnra yín yẹ ìkànnì àṣẹ wọn wò, ẹ má sì sanwó láti rí iṣẹ́ láé.",
      ig: "Ndị were ọrụ n'ezie, embassy na ndị na-enye scholarship anaghị arịọ gị ka ị kwụọ ego fọm, medical ma ọ bụ 'CoS' n'akaụntụ onye ọ bụla. Lelee weebụsaịtị ha n'onwe gị, akwụkwala ego iji nweta ọrụ.",
      ha: "Ma'aikata, ofisoshin jakadanci da masu ba da tallafin karatu na gaske ba sa neman ka biya kuɗin fom, medical ko 'CoS' zuwa asusun wani mutum. Duba shafinsu na hukuma da kanka, kuma kada ka taɓa biyan kuɗi don samun aiki."
    },
    romance_yahoo: {
      en: "Someone you've only met online who needs money for customs, a package, gift cards or a hospital bill is almost always a scammer. Don't send money; reverse-search their photos and talk to someone you trust.",
      pcm: "Person wey you only know online wey dey ask money for customs, package, gift card or hospital bill, na almost always yahoo. No send money; search their picture for Google and talk to person wey you trust.",
      yo: "Ẹni tí ẹ mọ̀ lórí ayélujára nìkan tó ń béèrè owó fún customs, ẹrù, gift card tàbí owó ilé-ìwòsàn, jìbìtì ni ní ọ̀pọ̀ ìgbà. Ẹ má fi owó ránṣẹ́; ẹ wá àwòrán wọn lórí Google, kí ẹ sì bá ẹni tí ẹ fọkàn tán sọ̀rọ̀.",
      ig: "Onye ị maara naanị n'ịntanetị nke na-arịọ ego maka customs, ngwugwu, gift card ma ọ bụ ụgwọ ụlọ ọgwụ na-abụkarị onye aghụghọ. Ezigala ego; chọọ foto ha na Google ma gwa onye ị tụkwasịrị obi.",
      ha: "Wanda ka sani a intanet kaɗai da ke neman kuɗi don kwastam, kunshin kaya, gift card ko kuɗin asibiti, kusan koyaushe ɗan damfara ne. Kada ka tura kuɗi; bincika hotunansa a Google kuma ka yi magana da wanda ka amince da shi."
    },
    fake_vendor_pos: {
      en: "Don't pay in full upfront to a vendor you can't verify. Use pay-on-delivery or a trusted platform, inspect the item first, and never pay a 'waybill' or 'redelivery' fee through a random link.",
      pcm: "No pay full money first give vendor wey you no fit confirm. Use pay-on-delivery or platform wey you trust, check the thing first, and no pay 'waybill' or 'redelivery' fee for any random link.",
      yo: "Ẹ má san gbogbo owó ṣáájú fún olùtajà tí ẹ kò lè fìdí rẹ̀ múlẹ̀. Ẹ lo 'pay on delivery' tàbí pèpéle tí ẹ fọkàn tán, ẹ yẹ ọjà wò kí ẹ tó sanwó, ẹ má sì san owó 'waybill' tàbí 'redelivery' lórí link àjèjì.",
      ig: "Akwụla ego zuru ezu tupu oge eru nye onye na-ere ahịa ị na-enweghị ike ịkwado. Jiri pay-on-delivery ma ọ bụ ebe ị tụkwasịrị obi, buru ụzọ lelee ngwa ahịa ahụ, akwụkwala ego 'waybill' ma ọ bụ 'redelivery' site na link ọ bụla.",
      ha: "Kada ka biya duka kuɗi tun farko ga ɗan kasuwar da ba za ka iya tabbatarwa ba. Yi amfani da pay-on-delivery ko dandalin da ka amince da shi, duba kayan tukuna, kuma kada ka biya kuɗin 'waybill' ko 'redelivery' ta wani link."
    },
    giveaway_grant: {
      en: "The government, CBN and big brands don't hand out cash through WhatsApp links, and real grants never charge a fee. Don't forward it, don't enter card details, and don't pay anything to 'claim'.",
      pcm: "Government, CBN and big company no dey share money through WhatsApp link, and real grant no dey collect fee. No forward am, no put your card details, and no pay anything to 'claim'.",
      yo: "Ìjọba, CBN àti àwọn ilé-iṣẹ́ ńlá kì í pín owó nípasẹ̀ link WhatsApp, grant gidi kò sì ní gba owó lọ́wọ́ yín. Ẹ má fi ránṣẹ́ sí àwọn mìíràn, ẹ má tẹ àlàyé káàdì yín sí i, ẹ má sì san owó kankan láti 'gbà á'.",
      ig: "Gọọmentị, CBN na nnukwu ụlọ ọrụ anaghị ekesa ego site na link WhatsApp, grant n'ezie anaghị anara ego. Ezigala ya ndị ọzọ, etinyela nkọwa kaadị gị, akwụkwala ego ọ bụla iji 'nweta' ya.",
      ha: "Gwamnati, CBN da manyan kamfanoni ba sa raba kuɗi ta link na WhatsApp, kuma tallafi na gaske ba ya karɓar kuɗi. Kada ka tura shi ga wasu, kada ka saka bayanan katinka, kuma kada ka biya komai don 'karɓa'."
    },
    _scam: {
      en: "Don't share any OTP, PIN, BVN or password. Don't click links or pay anyone until you confirm through your bank's official app or the number on the back of your card.",
      pcm: "No give anybody your OTP, PIN, BVN or password. No click link or pay money until you confirm am for your bank app or the number wey dey back of your card.",
      yo: "Ẹ má fún ẹnikẹ́ni ní OTP, PIN, BVN tàbí password yín. Ẹ má tẹ link tàbí san owó títí ẹ ó fi fìdí rẹ̀ múlẹ̀ nípasẹ̀ app banki yín tàbí nọ́mbà tó wà lẹ́yìn káàdì yín.",
      ig: "Enyela onye ọ bụla OTP, PIN, BVN ma ọ bụ password gị. Apịala link ma ọ bụ kwụọ onye ọ bụla ego ruo mgbe i kwadoro ya site n'app ụlọ akụ gị ma ọ bụ nọmba dị n'azụ kaadị gị.",
      ha: "Kada ka ba kowa OTP, PIN, BVN ko password ɗinka. Kada ka danna link ko ka biya kowa kuɗi sai ka tabbatar ta manhajar bankinka ko lambar da ke bayan katinka."
    },
    _legit: {
      en: "This looks like a normal message. Still, never share your OTP, PIN or BVN, and if anything asks for money or a code, confirm through the official app or number first.",
      pcm: "This one be like normal message. But still, no give anybody your OTP, PIN or BVN, and if anything ask for money or code, confirm am first for the official app or number.",
      yo: "Ìfiránṣẹ́ yìí dàbí èyí tó wọ́pọ̀. Síbẹ̀, ẹ má fún ẹnikẹ́ni ní OTP, PIN tàbí BVN yín, tí ohunkóhun bá sì béèrè owó tàbí kóòdù, ẹ kọ́kọ́ fìdí rẹ̀ múlẹ̀ nípasẹ̀ app tàbí nọ́mbà àṣẹ.",
      ig: "Ozi a dị ka ozi nkịtị. Ka o sina dị, enyela onye ọ bụla OTP, PIN ma ọ bụ BVN gị, ọ bụrụ na ihe ọ bụla arịọ ego ma ọ bụ koodu, buru ụzọ kwado ya site n'app ma ọ bụ nọmba ha kwadoro.",
      ha: "Wannan yana kama da saƙo na yau da kullum. Duk da haka, kada ka ba kowa OTP, PIN ko BVN ɗinka, kuma idan wani abu ya nemi kuɗi ko lamba, ka fara tabbatarwa ta manhaja ko lambar hukuma."
    }
  },

  examples: [
    ["🏦 BVN blocked", "Dear customer, your BVN has been restricted by CBN. Click bit.ly/bvn-ng24 to update within 24hrs or your account will be blocked."],
    ["💸 Fake alert", "Oga I don send the N85,000. Na network delay, e go reflect. Abeg release the goods make my driver carry am sharp sharp."],
    ["📈 AI trading", "Join our AI trading platform, 10% daily profit guaranteed, no risk. Withdrawal open after you pay 5% tax."],
    ["📈 Yorùbá", "Ẹ fi ₦50,000 sí platform AI trading wa, ẹ máa gba ₦5,000 lójoojúmọ́. Kò sí ewu rárá."],
    ["📱 Loan app", "Pay today or we go send your photo to all your contacts say you be FRAUDSTER."],
    ["💼 Fake job", "Congratulations! You have been shortlisted for NNPC graduate trainee. Pay N15,000 medical fee to Mr Bello account to confirm."],
    ["💸 Hausa", "Sannu, an samu payment ₦33,300 a asusunka, amma akwai ₦3,300 extra. Don complete, ka send to 09**...6789 via WhatsApp now."],
    ["✅ Bank alert", "Acct:01******89 Amt:NGN5,000.00 DR Desc:NIP/TRF TO ADEBAYO T Date:08-Oct-26 Avail Bal:NGN43,210.50"],
    ["✅ Family", "Mama, I don reach hostel o. I go call you after lecture tomorrow. Greet Papa for me."]
  ]
};
if (typeof module !== "undefined") module.exports = SHORA_I18N;
