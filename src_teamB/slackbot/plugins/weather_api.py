#encoding:utf-8
import urllib.request
import sys
import json

# get weather api
class get_weather():

#    try:
#        citycode = sys.argv[1]
#
#    except:
#        citycode = '130010' #デフォルト地域

#    resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()

    # 読み込んだJSONデータをディクショナリ型に変換
#    resp = json.loads(resp.read().decode('utf8'))


    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=080020'
    html = urllib.request.urlopen(url)
    resp = json.loads(html.read().decode('utf-8'))

    for forecast in resp['forecasts']:
        print(forecast['dateLabel'])

#    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=080020'
#    response = urllib.request.urlopen(url)
#    resp = json.loads(response.read().decode('utf-8'))

#    returnMessage = '**************************' + '\\n'
#    returnMessage += resp['title']+'\\n'
#    returnMessage += '**************************'+'\\n'
#    returnMessage += resp['description']['text']+'\\n'

#    for forecast in resp['forecasts']:
#        returnMessage += '**************************'+'\\n'
#        returnMessage += forecast['dateLabel']+'('+forecast['date']+')'+'\\n'
#        returnMessage += forecast['telop']+'\\n'
#        returnMessage += '**************************'+'\\n'
#    print("test")
