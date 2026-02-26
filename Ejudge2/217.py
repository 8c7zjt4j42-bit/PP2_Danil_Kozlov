n = int(input())
freq = {}
for _ in range(n):
    phone = input().strip()
    freq[phone] = freq.get(phone, 0) + 1

ans = 0
for c in freq.values():
    if c == 3:
        ans += 1

print(ans)
