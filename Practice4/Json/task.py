import json


with open("sample.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 60)


for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    speed = attrs["fecMode"]
    mtu = attrs["mtu"]

    print(dn, speed, mtu)