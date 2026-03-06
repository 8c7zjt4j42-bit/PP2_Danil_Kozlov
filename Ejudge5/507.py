import re

S = input()
P = input()
R = input()

result = re.sub(P, R, S)

print(result)