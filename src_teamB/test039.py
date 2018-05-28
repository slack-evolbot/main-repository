import re
import urllib.request
from bs4 import BeautifulSoup

#url = "https://ja.wikipedia.org/wiki/" + urllib.parse.quote_plus('新宿区', encoding='utf-8')
url = "https://www.weblio.jp/content/" + urllib.parse.quote_plus('放火', encoding='utf-8')
print(url)
f = urllib.request.urlopen(url)
html = f.read().decode('utf-8')

#soup = BeautifulSoup(html, "html.parser")
soup = BeautifulSoup(html, "html.parser")

#print(soup.head)
#print(soup.head.meta)

tmps = soup.body.find_all("li")

#, text.re.compile("[()]")

print(tmps)


print(soup.title)
print(soup.title.name)
print(soup.title.string)
