import urllib.request
import json

url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=080020'
html = urllib.request.urlopen(url)
resp = json.loads(html.read().decode('utf-8'))

for forecast in resp['forecasts']:
    print(forecast['dateLabel'])
