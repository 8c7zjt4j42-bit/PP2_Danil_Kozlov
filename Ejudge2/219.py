n = int(input())
total = {}

for _ in range(n):
    name, k = input().split()
    k = int(k)
    total[name] = total.get(name, 0) + k

for name in sorted(total.keys()):
    print(name, total[name])
