N = int(input())

x = 1
out = []
while x <= N:
    out.append(str(x))
    x *= 2

print(" ".join(out))
