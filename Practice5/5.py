import re

text = input("Enter string: ")

pattern = r'^a.*b$'

if re.match(pattern, text):
    print("Match")
else:
    print("No match")