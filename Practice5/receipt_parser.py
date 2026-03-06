import re
import json

# 0
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

result = {}

# 1
prices = re.findall(r'\b\d[\d\s]*,\d{2}\b', text)


prices_float = []
for p in prices:
    p = p.replace(" ", "").replace(",", ".")
    prices_float.append(float(p))

result["prices"] = prices_float


# 2
items = re.findall(r'\d+\.\n(.+)', text)
result["items"] = items


# 3
total_match = re.search(r'ИТОГО:\s*\n([\d\s]+,\d{2})', text)

if total_match:
    total = total_match.group(1)
    total = total.replace(" ", "").replace(",", ".")
    result["total"] = float(total)


# 4
datetime_match = re.search(
    r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', text
)

if datetime_match:
    result["datetime"] = datetime_match.group(1)


# 5
payment_match = re.search(r'(Банковская карта|Наличные)', text)

if payment_match:
    result["payment_method"] = payment_match.group(1)



print(json.dumps(result, ensure_ascii=False, indent=2))