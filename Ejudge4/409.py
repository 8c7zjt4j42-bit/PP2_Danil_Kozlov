def powers(n):
    for i in range(n+1):
        yield 2**i

n = int(input())
print(" ".join(str(x) for x in powers(n)))