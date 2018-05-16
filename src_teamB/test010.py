import re

pattern = re.compile(r'.*') 
print(str(pattern.match('54321')==True))
