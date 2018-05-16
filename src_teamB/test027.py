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
lat = "35.6881792";
lng = "139.69609";
#url = "http://maps.google.com/maps/api/staticmap?center=" + lat + "," + lng + "&zoom=13&size=640x480&markers=" + lat + "%2C" + lng + "&sensor=false&key=AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg";
#url = "http://maps.google.com/maps/api/staticmap?center=" + lat + "," + lng + "&zoom=18&size=640x480&markers=" + lat + "%2C" + lng + "&sensor=false&optimizeWaypoints=true&key=AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg";

url="https://maps.googleapis.com/maps/api/staticmap?path=weight%3A10%7Ccolor%3Ared%7C" + lat + "%2C" + lng + "%7C" + "35" + "%2C" + "139" + "&size=600x450&key=AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg"

print(url)

download_pic(url,address)