def cycle_list(lst, k):
    for _ in range(k):
        for x in lst:
            yield x

lst = input().split()
k = int(input())
print(" ".join(str(x) for x in cycle_list(lst, k)))