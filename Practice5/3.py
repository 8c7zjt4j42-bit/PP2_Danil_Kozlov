import re

text = input("Enter text: ")

pattern = r'[a-z]+_[a-z]+'

print(re.findall(pattern, text))