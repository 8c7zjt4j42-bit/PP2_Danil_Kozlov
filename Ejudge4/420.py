g=0
n=0

m=int(input())
for _ in range(m):
    scope,val=input().split()
    val=int(val)
    if scope=="global":
        g+=val
    elif scope=="nonlocal":
        n+=val
    else:
        x=val  

print(g,n)