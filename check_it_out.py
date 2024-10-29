import re
from pprint import pprint

regex = r"\((.+?)\)"

with open('C:\\set2\\1.txt', 'r', encoding="UTF-8") as file:
    content = [line.strip() for line in file.readlines() if line.strip()]

lst = []
for i in content:
    match = re.findall(regex, i)
    if match:
        lst.extend(match)

codes = list(filter(lambda string: string[0].isdigit(), lst))
print(codes)
