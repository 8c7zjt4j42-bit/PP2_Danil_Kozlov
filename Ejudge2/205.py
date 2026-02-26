n = int(input())

while n % 2 == 0 and n > 1:
    n //= 2

print("YES" if n == 1 else "NO")
