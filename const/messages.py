from utils.rabbit import Rabbit

MSG_INITIAL_GREETING = Rabbit.uni2zg(
    "မင်္ဂလာပါ မြန်မာလို Pass အခြေအနေ စစ်ဆေးပေးမယ့်ကိုရွှေ မှ ကြိုဆို ပါတယ်အောက်မှာပြထားတဲ့ ခလုပ်လေးတွေကိုနှိပ်ပြီးစစ်လို့ရပါတယ်" \
    "ခုလောလောဆယ်တော့ S Pass နဲ့ E Pass ကို သာစစ်လို့ရမှာဖြစ် ပြီး WP(Work Permit) ကတော့ ရမှာမဟုတ်သေးတဲ့ အတွက်တောင်းပန်ပါတယ်။")
MSG_GOOD_BYE = Rabbit.uni2zg("အလုပ်အကိုင်တွေအားလုံးအဆင် ပြေပါစေလို့ဆုမွန်ကောင်းတောင်း ပေးပါတယ်။")

MSG_PP_CHECK_INSTRUCTION = Rabbit.uni2zg(
    "ကောင်းပြီ သင့်ရဲ့ Passport နံပါတ် ကို အခုချက်ဘောက်စ်မှာရိုက်ထည့်ပြီး ခဏလေးစောင့်ပေးပါ")

MSG_INVALID_PP_NO = Rabbit.uni2zg("ပတ်စ်ပို့ နံပတ်ရိုက်တာမှားနေပါတယ် ပြန်စစ်ကြည့်ပါအုန်း")

MSG_WELL_PRESS_BELOW = Rabbit.uni2zg("ကဲဟုတ်ပါပြီ အောက်ကခလုပ်လေးတွေကို နှိပ်ပြီးမေးလို့ရပြီ")

MSG_ABOUT_US = Rabbit.uni2zg(
    "ကျွန်တော်တို့ ကတော့ ဒီစင်ကာပူမှာ အလုပ်လုပ်နေကြတဲ့ ဆော့ဝဲ ရေးသားသူများပါ။ ဒီ Messenger Bot Application " \
    "ကိုလုပ်ဖြစ်တာ တနေ့တနေ့ IPA Letter အတုမိပြီးလေဆိပ်ရောက်မှလှည့်ပြန်ရတာမျိုးတွေ " \
    "ကျွန်တော်တို့မြင်တွေ့နေရတော့ နောက်လူတွေအလိမ်မခံရအောင် ဘယ်လိုလုပ်မလဲဆိုပြီး စဉ်းစားမိရင်းနဲ့ " \
    "လုပ်ဖြစ်သွားတာပါ။ တချို့က စင်ကာပူ MOM Website " \
    "မှာစစ်ရကောင်းမှန်းမသိကြဘူး " \
    "တချို့ကလဲသိတယ် သို့သော် ဘယ်လိုရှာရမှန်းမသိ စသဖြင့်ပေါ့လေ။ကျနော်တို့ Messenger မှာတော့ Passport " \
    "နံပါတ်ရိုက်လိုက်တာနဲ့ MOM website မှာ သွားစစ်ပေးမှာပါ Pass အခြေအနေ သိရမယ် တကယ် လျောက်ထားလား Reject " \
    "လား Pending လား စသဖြင့် နာမည်နှင့် တကွ ဖော်ပြပေးမှာပါ။")

MSG_PRIVACY_POLICY = Rabbit.uni2zg("ဤMessenger Application သည် MOM ၏ တရားဝင် Application မဟုတ်ပါ\n" \
                                   "အားလုံးလွယ်ကူစွာစစ်ဆေးနိုင် စေရန် ရည်ရွယ်ချက်ဖြင့် သာပြုလုပ်ထားခြင်းဖြစ်ပါသည်။\n" \
                                   "ဤMessenger Application တွင်ပါဝင်ပတ်သက်နေသည့် Passport နံပတ်များကို မည်သည့်နည်းနှင့် မျှ\n" \
                                   "သိမ်းဆည်းထားခြင်းမရှိကြောင်း အာမခံပါသည်။ အချက်အလက်များကိုလည်း MOM website မှ " \
                                   "တိုက်ရိုက်ယူထားခြင်းဖြစ်ပြီး အချက်အလက်များကို " \
                                   "မည်သည့်နည်းနှင့်မျှပြုပြင်ပြောင်းလဲသိမ်းဆည်းထားခြင်းမရှိပါ။")

MSG_LICENSE = Rabbit.uni2zg(
    "ဤMessenger Source Code ကို လည်း အများပြည်သူကြည့်ရှုနိုင်ရန်အလို့ငှာ Github တွင်တင်ထားပါသည်\n" \
    "အချက်အလက်များ ရယူသည့် Website\n" \
    "https://eponline.mom.gov.sg/epol/PEPOLENQM008SubmitAction.do\n" \
    "Opensource License များ\n" \
    "MIT License: https://github.com/Rabbit-Converter/Rabbit-Python \n" \
    "MIT License: https://github.com/gawel/pyquery\n" \
    "Apache License : https://github.com/tornadoweb/tornado\n" \
    "Apache License : V2https://github.com/requests/requests/\n")

MSG_RECORD_NOT_FOUND = Rabbit.uni2zg("ယခုပတ်စပို့နံပတ်နဲ့ သက်ဆိုင်တဲ့ အချက်အလက်ကိုရှာမတွေ့ပါ။\n " \
                                     "သို့မဟုတ် (WP)Work Permit အမျိုးအစား ကို လောလောဆယ်စစ်လို့မရသေးပါခင်ဗျာ အဆင်မပြေမှုများအတွက်တောင်းပန်ပါတယ်ခင်ဗျာ။" \
                                     "အရမ်းစိတ်မပူပါနဲ့ သေချာအောင် https://eponline.mom.gov.sg/epol/PEPOLENQM008SubmitAction.do မှာစစ်ကြည့်ပါအုန်း")

MSG_RECORD_EXISTS = Rabbit.uni2zg("အမည်။  ။  {} \n" \
                                  "PASS လျှောက်လွှာနံပါတ်။  ။ {}\n" \
                                  "PASS တင်သည့်ရက်စွဲ။  ။ {}\n" \
                                  "PASS အမျိုးအစား။  ။ {}\n" \
                                  "PASS အခြေအနေ။  ။ {} ပါ\n" \
                                  "ထပ်မံသေချာ အောင် https://eponline.mom.gov.sg/epol/PEPOLENQM008SubmitAction.do မှာစစ်ကြည့်ပါအုန်း\n" \
                                  "{}")

MSG_SERVICE_UNAVAILABLE = Rabbit.uni2zg("PASS စစ်ဆေးခြင်း ဝန်ဆောင်မှု မရနိုင်သေးပါ\n" \
                                        "စစ်ဆေးနိုင်မည့်အချိန်တွေကတော့\nတနင်္လာနေ့ မှ သောကြာနေ့ တွင် နံနက် ၈ : ၀၀ - ည ၈ : ၀၀ အထိ : \nစနေနေ့တွင် နံနက် ၈ : ၀၀ - ညနေ ၂ : ၀၀ အတွင်းသာ\nစစ်လို့ရပါတယ်")

MSG_INTERNAL_SERVER_ERROR = Rabbit.uni2zg(
    "တောင်းပန်ပါတယ် ရှာဖွေနေစဉ် စနစ်မှာ မှားယွင်းမှုတခုဖြစ်သွားလို့ အစကပြန်စပေးပါ။\n" \
    "ကျေးဇူးတင်ပါတယ်")
