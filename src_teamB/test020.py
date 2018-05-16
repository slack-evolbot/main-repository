from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import json
import time 
import urllib
import re
import sys
import argparse

def getImageCategory(fname, modelName):

    register_openers()

    APIKEY = "664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444"
    url = 'https://api.apigw.smt.docomo.ne.jp/imageRecognition/v1/concept/classify/?APIKEY=' + APIKEY

    f = open(fname, 'r')

    datagen, headers = multipart_encode({"image": f, 'modelName': modelName})
    request = urllib2.Request(url,datagen, headers)
    response = urllib2.urlopen(request)

    res_dat = response.read()

    return json.loads(res_dat)['candidates']


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--image'    , dest='image', type=str, default='rose.jpg', help='name of input image')
    parser.add_argument('--model'    , dest='model', type=str, default='scene', help='modelName = {scene, fashion_pattern, fashion_type, fashion_style, fashion_color, food, flower, kinoko}')

    args = parser.parse_args()

    fname = args.image
    model_name = args.model

    candidate_list = getImageCategory(fname, model_name)

    for can in candidate_list:
        print can['tag'], can['score']
