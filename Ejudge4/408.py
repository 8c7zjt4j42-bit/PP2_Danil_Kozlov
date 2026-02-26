def primes(n):
    for x in range(2, n+1):
        ok = True
        for d in range(2, int(x**0.5)+1):
            if x % d == 0:
                ok = False
                break
        if ok:
            yield x

n = int(input())
print(" ".join(str(x) for x in primes(n)))