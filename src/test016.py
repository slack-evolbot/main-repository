import urllib.request
from urllib.parse import urlparse
import json

url = 'https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?q=ブラジルの母国語は？&APIKEY=664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444'
p = urlparse(url)
query = urllib.parse.quote_plus(p.query, safe='=&')
url = '{}://{}{}{}{}{}{}{}{}'.format(
    p.scheme, p.netloc, p.path,
    ';' if p.params else '', p.params,
    '?' if p.query else '', query,
    '#' if p.fragment else '', p.fragment)

print(url)

response = urllib.request.urlopen(url)
response = json.loads(response.read().decode("utf-8"))
print(response['message']['textForDisplay'])
