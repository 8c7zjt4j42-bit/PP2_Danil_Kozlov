import json
import re

data = json.loads(input())
q = int(input())

for _ in range(q):
    path = input().strip()
    cur = data
    ok = True
    
    
    tokens = re.findall(r'[^\.\[\]]+|\[\d+\]', path)
    
    for t in tokens:
        if t.startswith('['):   
            idx = int(t[1:-1])
            if isinstance(cur, list) and 0 <= idx < len(cur):
                cur = cur[idx]
            else:
                ok = False
                break
        else:                   
            if isinstance(cur, dict) and t in cur:
                cur = cur[t]
            else:
                ok = False
                break
    
    if ok:
        print(json.dumps(cur, ensure_ascii=False, separators=(',', ':')))
    else:
        print("NOT_FOUND")