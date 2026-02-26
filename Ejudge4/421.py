import importlib

q=int(input())
for _ in range(q):
    mod,attr=input().split()
    try:
        m=importlib.import_module(mod)
    except:
        print("MODULE_NOT_FOUND")
        continue
    if not hasattr(m,attr):
        print("ATTRIBUTE_NOT_FOUND")
    else:
        print("CALLABLE" if callable(getattr(m,attr)) else "VALUE")