def gen(n):
    i = 0
    first = True
    while i <= n:
        if i % 12 == 0:
            if not first:
                print(" ", end="")
            print(i, end="")
            first = False
        i += 1

n = int(input())
gen(n)