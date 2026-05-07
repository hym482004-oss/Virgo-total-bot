import re

# =====================
# 🔥 RULE KEYWORDS
# =====================
RULES = {
    "r": ["r", "အာ"],
    "pat": ["ပတ်", "ပါ", "ပတ်သီး", "အပါ", "p", "by", "bi", "ch"],
    "pat_pu": ["ပတ်ပူး", "ပူးပို", "ပတ်ပူးပို", "ထန်", "ထပ်", "ထိပ်ပိတ်", "ထိပ်နောက်"],
    "top": ["ထိပ်", "ထ", "top", "t"],
    "brake": ["ဘရိတ်", "bk"],
    "even_brake": ["စုံဘရိတ်", "စဘရိတ်", "စုံbk", "မbk", "မဘရိတ်"],
    "khwe": ["ခွေ", "ခ", "အခွေ"],
    "khwe_pu": ["ခွေပူး", "အပူးပါ", "အပူးအပြီးပါ"],
    "power": ["ပါဝါ", "pw", "ပဝ", "power"],
    "nk": ["နက္ခတ်", "nk", "နက်", "နခ"],
    "bro": ["ညီကို", "ညီအကို", "ညီအစ်ကို"],
    "pait": ["ပိတ်", "အပိတ်", "ပိတိ", "ပ"],
    "ma_pu": ["မပူး", "မပိတ်"],
    "so_pu": ["စုံပူး"],
    "double": ["အပူး", "ပူး"],
    "sam": ["စမ", "စစ", "မမ", "စုံစုံ", "စုံမ", "မစုံ"],
    "khap": ["ခပ်"],
    "kap": ["ကပ်", "ကို", "အကပ်"],
    "ten": ["ဆယ်ပြည့်"]
}

# =====================
# 🔥 NORMALIZE
# =====================
def normalize(text):
    return text.lower()

# =====================
# 🔥 CLEAN TEXT
# =====================
def clean_text(text):
    # Remove market names to avoid counting as numbers
    text = re.sub(r'\b(me|mega|မီ|မီဂါ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(du|dubai|ဒူ|ဒူဘိုင်း)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(mm)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(lao|laos|loadon|laodon|လာအို|လာလာ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(ld|london|လန်ဒန်|လန်လန်)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(glo|global|ဂလို)\s*\d+\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(maxi|max|မက်ဆီ|မက်စီ|စီစီ)\s*\d+\b', '', text, flags=re.IGNORECASE)
    return text

# =====================
# 🔥 EXTRACT
# =====================
def extract_numbers(text):
    return re.findall(r"\d+", text)

def extract_price_full(text):
    """
    Return price: take number after R or last number
    """
    match_rev = re.search(r'[rR]\s*(\d+)', text)
    if match_rev:
        p = int(match_rev.group(1))
        return p, p
    
    numbers = re.findall(r"\d+", text)
    if numbers:
        last_num = int(numbers[-1])
        return last_num, last_num
    
    return 0, 0

# =====================
# 🔥 RULE DETECT
# =====================
def detect_rule(text):
    text_lower = text.lower()
    for rule, keys in RULES.items():
        for k in keys:
            if k in text_lower:
                return rule
    return "direct"

# =====================
# 🔥 CALC ENGINE
# =====================
def calculate(rule, nums, price_norm, price_rev, line):

    n = len(nums)
    base = 0

    if rule == "khwe":
        # ခွေ = n x (n-1)
        base = n * (n - 1)
    elif rule == "khwe_pu":
        # ခွေပူး = n x n
        if nums:
            all_digits = ''.join(map(str, nums))
            count = len(all_digits)
            base = count * count
        else:
            base = 0
    elif rule == "pat":
        # ပါ / ပတ် = 19 ကွက်
        base = 19
    elif rule == "pat_pu":
        # ပတ်ပူး = 20 ကွက်
        base = 20
    elif rule == "top":
        # ထိပ် = တစ်လုံးကို 10 ကွက်
        if nums:
            count = len(nums)
            base = count * 10
        else:
            base = 10
    elif rule == "brake":
        # ဘရိတ် / bk = တစ်လုံးကို 10 ကွက်
        if nums:
            count = len(nums)
            base = count * 10
        else:
            base = 10
    elif rule == "even_brake":
        # စုံဘရိတ် = 50 ကွက်
        base = 50
    elif rule == "power":
        # ပါဝါ = 10 ကွက်
        base = 10
    elif rule == "nk":
        # နက္ခတ် = 10 ကွက်
        base = 10
    elif rule == "bro":
        # ညီကို = 20 ကွက်
        base = 20
    elif rule == "pait":
        # ပိတ် = 10 ကွက်
        base = 10
    elif rule == "ma_pu":
        # မပူး / မပိတ် = 50 ကွက်
        base = 50
    elif rule == "so_pu":
        # စုံပူး = 5 ကွက်
        base = 5
    elif rule == "double":
        # အပူး = 10 ကွက်
        base = 10
    elif rule == "sam":
        # စမ စစ မမ etc = 25 ကွက်
        base = 25
    elif rule == "khap":
        # ခပ် = n x n
        if nums:
            n_digit = len(str(nums[0]))
            base = n_digit * n_digit
        else:
            base = 0
    elif rule == "kap":
        # ကပ် = ဘယ်ဂဏန်းရေ x ညာဂဏန်းရေ
        if len(nums) >= 2:
            part1 = str(nums[0])
            part2 = str(nums[1])
            base = len(part1) * len(part2)
        else:
            base = 0
    elif rule == "ten":
        # ဆယ်ပြည့် = 10 ကွက်
        base = 10
    else: # direct
        # သာမန်ဂဏန်း = ကွက်ရေ
        base = len(nums) if nums else 0

    # ❌ VALIDATION: 2D မဟုတ်တဲ့ ဂဏန်းတစ်လုံးတည်း (1,2,3...) မတွက်
    if len(nums) == 1 and len(str(nums[0])) == 1:
        # အချိန် (4:30) လိုမျိုးတွေပါ စစ်
        if ":" in line or "." in line:
            base = 0
        else:
            # 1 လုံးတည်းဆို error ပြဖို့ return -1
            return -1, 0

    # --- Reverse Check ---
    is_reverse = bool(re.search(r'r|အာ', line, re.IGNORECASE))
    
    total = base * price_norm
    if is_reverse:
        total += base * price_norm # R ဆို နှစ်ခါတွက်

    return base, total


# =====================
# 🔥 MAIN PARSE
# =====================
def parse_message(text):

    raw_text = text
    work_text = clean_text(normalize(text))

    # Split by symbols (space, -, *, /, ., :, =)
    work_text = work_text.replace("=", "\n")
    work_text = work_text.replace("-", "\n")
    work_text = work_text.replace("*", "\n")
    work_text = work_text.replace("/", "\n")
    work_text = work_text.replace(".", "\n")
    work_text = work_text.replace(":", "\n")
    lines = work_text.splitlines()

    results = []
    grand_total = 0
    has_error = False

    # Get Price ONCE from full text
    price_norm, price_rev = extract_price_full(raw_text)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        nums = extract_numbers(line)
        rule = detect_rule(line)

        base, total = calculate(rule, nums, price_norm, price_rev, line)

        if base == -1:
            has_error = True
            break

        grand_total += total

        results.append({
            "raw": line,
            "rule": rule,
            "base": base,
            "amount": price_norm,
            "total": int(total)
        })

    return {
        "lines": results,
        "grand_total": int(grand_total),
        "has_error": has_error
    }
