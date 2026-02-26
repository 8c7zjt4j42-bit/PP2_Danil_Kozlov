import json

A = json.loads(input())
B = json.loads(input())

def jdump(v):
   
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'), sort_keys=True)

out = []

def walk(path, a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        keys = set(a.keys()) | set(b.keys())
        for k in keys:
            new_path = path + [k]
            in_a = k in a
            in_b = k in b
            if in_a and in_b:
                walk(new_path, a[k], b[k])
            elif in_a and not in_b:
                out.append((".".join(new_path), f"{'.'.join(new_path)} : {jdump(a[k])} -> <missing>"))
            else:
                out.append((".".join(new_path), f"{'.'.join(new_path)} : <missing> -> {jdump(b[k])}"))
    else:
        if a != b:
            p = ".".join(path)
            out.append((p, f"{p} : {jdump(a)} -> {jdump(b)}"))

walk([], A, B)

if not out:
    print("No differences")
else:
    out.sort(key=lambda x: x[0])
    for _, line in out:
        print(line)