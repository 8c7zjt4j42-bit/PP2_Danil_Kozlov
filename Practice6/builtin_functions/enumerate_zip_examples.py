names = ["Alice", "Bob", "Charlie"]


print("Enumerate:")
for i, name in enumerate(names):
    print(i, name)


nums1 = [1, 2, 3]
nums2 = [4, 5, 6]

zipped = list(zip(nums1, nums2))
print("\nZipped:", zipped)


num_str = "123"
num_int = int(num_str)

print("\nType conversion:")
print(num_str, type(num_str))
print(num_int, type(num_int))