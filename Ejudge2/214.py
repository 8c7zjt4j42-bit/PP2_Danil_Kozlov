n = int(input())
arr = list(map(int, input().split()))

freq = {}
for v in arr:
    freq[v] = freq.get(v, 0) + 1

best_val = None
best_cnt = -1

for v, c in freq.items():
    if c > best_cnt or (c == best_cnt and (best_val is None or v < best_val)):
        best_cnt = c
        best_val = v

print(best_val)
