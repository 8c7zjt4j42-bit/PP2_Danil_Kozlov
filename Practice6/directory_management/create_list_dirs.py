import os

os.makedirs("test_folder/subfolder", exist_ok=True)


print("Current directory:", os.getcwd())


print("Contents:")
for item in os.listdir("."):
    print(item)


print("\nTXT files:")
for file in os.listdir("."):
    if file.endswith(".txt"):
        print(file)