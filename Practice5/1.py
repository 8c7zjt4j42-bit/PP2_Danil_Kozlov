import re

text = input("Enter string: ")

pattern = r'^ab*'

if re.match(pattern, text):
    print("Match found")
else:
    print("No match")