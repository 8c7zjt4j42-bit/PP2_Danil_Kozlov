import shutil
import os

shutil.copy("data.txt", "copy.txt")
print("File copied")

if os.path.exists("copy.txt"):
    os.remove("copy.txt")
    print("File deleted")
else:
    print("File not found")