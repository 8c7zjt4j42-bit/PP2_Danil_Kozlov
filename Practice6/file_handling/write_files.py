with open("data.txt", "w") as f:
    f.write("Hello\n")
    f.write("World\n")

with open("data.txt", "a") as f:
    f.write("Appended line\n")

print("File written successfully")
