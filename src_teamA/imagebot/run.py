# coding: utf-8
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions, InceptionV3
import numpy as np
import json
from slackbot.bot import Bot
import threading
import os
import time
import glob
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

checked_flg = False

LABEL_JSON_PATH = './label.json'
IMAGENET_JSON_PATH = './imagenet_class_index.json'
SLEEP_TIME = 1

def check_img_file():
    print("画像監視スレッド開始")
    
    for filename in glob.glob('tmp.*'):
            os.remove(filename)
    if(os.path.exists(LABEL_JSON_PATH)):
            os.remove(LABEL_JSON_PATH)
    
    print("model読み込み開始")
    model = InceptionV3(weights='imagenet')
    print("model読み込み完了")
    print("Slackへ画像アップロード可能")
    
    global checked_flg
    while True:  
        tmpfile = None
        for filename in glob.glob('tmp.*'):
            tmpfile = filename
        if(tmpfile != None and not checked_flg):
            imagelabel2json(tmpfile, model)
            checked_flg = True
        if(tmpfile == None and checked_flg):
            checked_flg = False
        time.sleep(SLEEP_TIME)
            
def imagelabel2json(tmpfile, model):
    print("画像解析開始")

    img = image.load_img(tmpfile, target_size=(299, 299))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    
    recognize = decode_predictions(preds)
    en_label = recognize[0][0][1]
    label = en_label
    score = str(recognize[0][0][2])

    with open(IMAGENET_JSON_PATH, 'r') as f:
        obj = json.load(f)
        for i in obj:
            if i['en'] == en_label:
                label = i['ja']
                break
            
    dict = {
        'label': label,
        'score': score
    }
    
    f = open(LABEL_JSON_PATH, 'w')
    json.dump(dict, f)
    
    print("画像解析終了")

def main():
    bot = Bot()
    
    image_thread = threading.Thread(target=check_img_file)
    image_thread.setDaemon(True)
    image_thread.start()
    
    try:
        bot.run()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
    