import re

text = input("Enter camelCase string: ")

result = re.split(r'(?=[A-Z])', text)

print(result)