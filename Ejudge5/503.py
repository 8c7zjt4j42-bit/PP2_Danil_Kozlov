import re

S = input()
P = input()

matches = re.findall(P, S)
print(len(matches))