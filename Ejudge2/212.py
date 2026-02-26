n = int(input())
a = list(map(int, input().split()))
print(*[x * x for x in a])
