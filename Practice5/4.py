import re

text = input("Enter text: ")

pattern = r'[A-Z][a-z]+'

print(re.findall(pattern, text))