def word_to_number(s):
    digits = {
        "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
        "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
    }
    num = ""
    for i in range(0, len(s), 3):
        num += digits[s[i:i+3]]
    return int(num)

def number_to_word(n):
    digits = {
        "0": "ZER", "1": "ONE", "2": "TWO", "3": "THR", "4": "FOU",
        "5": "FIV", "6": "SIX", "7": "SEV", "8": "EIG", "9": "NIN"
    }
    result = ""
    for d in str(n):
        result += digits[d]
    return result

s = input().strip()

if '+' in s:
    a, b = s.split('+')
    result = word_to_number(a) + word_to_number(b)
elif '-' in s:
    a, b = s.split('-')
    result = word_to_number(a) - word_to_number(b)
elif '*' in s:
    a, b = s.split('*')
    result = word_to_number(a) * word_to_number(b)

print(number_to_word(result))