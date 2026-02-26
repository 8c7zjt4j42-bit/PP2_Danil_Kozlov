def even_gen(n):
    i = 0
    while i <= n:
        yield i
        i += 2

n = int(input())

first = True
for x in even_gen(n):
    if not first:
        print(",", end="")
    print(x, end="")
    first = False