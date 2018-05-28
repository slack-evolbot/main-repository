import re

line = ' 9  61.199.130.26 (61.199.130.26)  131.524 ms  131.494 ms  131.469 ms'

m = re.search('\d{1,3}.\d{1,3}.\d{1,3}', line)
#m = re.search(r'[0-9]', line)
if m:
    print("a"+m.group(0))
