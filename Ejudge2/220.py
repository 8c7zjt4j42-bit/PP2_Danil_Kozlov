import sys

data = sys.stdin.buffer.read().split()
n = int(data[0])

db = {}
out = []

i = 1
for _ in range(n):
    cmd = data[i].decode()
    if cmd == "set":
        key = data[i + 1].decode()
        value = data[i + 2].decode()
        db[key] = value
        i += 3
    else:  # get
        key = data[i + 1].decode()
        if key in db:
            out.append(db[key])
        else:
            out.append(f"KE: no key {key} found in the document")
        i += 2

sys.stdout.write("\n".join(out))