import urllib.request
import json

for i in range(100):
    num = '{0:06}'.format(i)
    try:
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + str(num)
        html = urllib.request.urlopen(url)
        resp = json.loads(html.read().decode('utf-8'))

        print(resp['title'])
    except HTTPError:
        aaa = "aaa"
