with open("data.txt", "r") as f:
    print("Full read:")
    print(f.read())

with open("data.txt", "r") as f:
    print("\nLine by line:")
    print(f.readline())
    print(f.readline())

with open("data.txt", "r") as f:
    print("\nReadlines:")
    lines = f.readlines()
    print(lines)