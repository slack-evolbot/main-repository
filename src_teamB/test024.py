# -*- coding: utf-8 -*-
import googlemaps
import re

gmaps = googlemaps.Client(key='AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg')

directions_result = gmaps.directions('東京都新宿区西新宿1-21-1 明宝ビル','新宿駅',mode="walking",alternatives=False,language="ja")

#print(directions_result)

#for step in directions_result['routes'][0]['legs'][0]['steps']:

print("目的地まで" + re.sub(" ", "", directions_result[0]['legs'][0]['distance']['text']) + "(" + directions_result[0]['legs'][0]['duration']['text'] + ")")

counter = 1
for step in directions_result[0]['legs'][0]['steps']:
    print('{0:02d}'.format(counter) + ". " + re.sub(" ", "", step['distance']['text']) + re.sub(r'[<b>\/]', "", step['html_instructions']))
    counter += 1

#for step in directions_result['legs']['steps']:
#    print(step['duration']['html_instructions'])
