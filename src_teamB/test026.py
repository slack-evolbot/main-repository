# -*- coding: utf-8 -*-
from pygeocoder import Geocoder
import urllib.request

def download_pic(url,filename):
    img = urllib.request.urlopen(url)
    localfile = open( "./map/" + str(filename) + ".png" , 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

address = '新宿　なか卯'
results = Geocoder.geocode(address)
print(results[0].coordinates)

result = Geocoder.reverse_geocode(*results.coordinates, language="ja")
print(result)

html1 = "https://maps.googleapis.com/maps/api/staticmap?center="
html2 = "&maptype=terrain&size=640x480&sensor=false&zoom=18&markers="
html3 = "&key=AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg"

axis = str((results[0].coordinates)[0]) + "," + str((results[0].coordinates)[1])

html = html1 + axis + html2 + axis + html3

print(html)

download_pic(html,address)
