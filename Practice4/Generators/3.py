def divisible(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

for x in divisible(100):
    print(x)