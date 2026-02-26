import json

def patch(src, p):
    for k, v in p.items():
        if v is None:
            src.pop(k, None)
        elif isinstance(v, dict) and isinstance(src.get(k), dict):
            patch(src[k], v)
        else:
            src[k] = v
    return src

source = json.loads(input())
patch_obj = json.loads(input())

res = patch(source, patch_obj)
print(json.dumps(res, separators=(',', ':'), sort_keys=True))