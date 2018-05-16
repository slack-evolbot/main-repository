import urllib.request
from urllib.parse import urlparse
import json

APP_URL = 'https://api.apigw.smt.docomo.ne.jp/knowledgeQA/v1/ask?q={}&APIKEY={}'

def get_knowledge(message, api_key):
    url = APP_URL.format(message, api_key)
    p = urlparse(url)
    query = urllib.parse.quote_plus(p.query, safe='=&')
    url = '{}://{}{}{}{}{}{}{}{}'.format(
        p.scheme, p.netloc, p.path,
        ';' if p.params else '', p.params,
        '?' if p.query else '', query,
        '#' if p.fragment else '', p.fragment)
    response = urllib.request.urlopen(url)
    response = json.loads(response.read().decode("utf-8"))

    return response['message']['textForDisplay']

def main(message):
    api_key = '664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444'
    resp = get_knowledge(message, api_key)

    return resp

if __name__ == "__main__":
    main()
