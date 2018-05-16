# -*- coding: utf-8 -*-
import googlemaps
import re
import datetime
import locale
import MySQLdb
import random

connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')

today = datetime.date.today()
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    
try:
    with connection.cursor() as cursor:
        
        sql = "SELECT SHOP_NAME, SPECIAL FROM SHINJUKU_LUNCH WHERE SERVICE_DAY = '" + str(today.day) + "' OR SERVICE_WEEK = '" + today.strftime('%a') + "';"
        
        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()

        if len(result) == 0:
            shop_name = "中本"
            special = "特に何もない"
        elif len(result) >= 2:
            ran = random.randint(0, len(result)-1)
            shop_name = result[ran][0]
            special = result[ran][1]
        else:
            shop_name = result[0][0]
            special = result[0][1]

        gmaps = googlemaps.Client(key='AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg')

        directions_result = gmaps.directions('東京都新宿区西新宿1-21-1 明宝ビル', "新宿 " + shop_name, mode="walking", alternatives=False, language="ja")

        print(directions_result)

        print("今日のおすすめは" + shop_name + "です")
        print(shop_name + "に行くと" + special)
        
        print(shop_name + "まで" + re.sub(" ", "", directions_result[0]['legs'][0]['distance']['text']) + "(" + directions_result[0]['legs'][0]['duration']['text'] + ")")

        counter = 1
        for step in directions_result[0]['legs'][0]['steps']:
            print('{0:02d}'.format(counter) + ". " + re.sub(" ", "", step['distance']['text']) + re.sub(r'[\x20-\x7E]+', "", re.sub("<div", "（", re.sub("</div>", "）", step['html_instructions']))))
            counter += 1

except Exception as e:
    print("予期せぬエラーが発生しました")
