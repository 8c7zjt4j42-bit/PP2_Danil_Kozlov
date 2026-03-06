import re

S = input()
P = input()

pattern = re.escape(P)

matches = re.findall(pattern, S)

print(len(matches))