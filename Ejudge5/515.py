import re

s = input()

def double_digit(match):
    d = match.group()
    return d + d

result = re.sub(r'\d', double_digit, s)

print(result)