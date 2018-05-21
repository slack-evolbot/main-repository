# coding: utf-8
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions, InceptionV3
import numpy as np
import json
import my_camera
import time

#物体名の日本語変換用JSON
IMAGENET_JSON_PATH = "./imagenet_class_index.json"
#一時的写真ファイルパス
PHOTO_PATH = "./img/tmp.jpg"
#モデルを事前読込み
model = InceptionV3(weights='imagenet')
mycamera = my_camera.MyCamera()

if __name__ == "__main__":
    #映像プレビュー開始
    mycamera.start_preview()
    
    try:
        while True:
            #InceptionV3で物体認識
            mycamera.take_picture(PHOTO_PATH)
            img = image.load_img(PHOTO_PATH, target_size=(299, 299))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = model.predict(x)
            
            recognize = decode_predictions(preds)
            en_label = recognize[0][0][1]
            label = en_label
            score = str(recognize[0][0][2])

            #日本語化
            with open(IMAGENET_JSON_PATH, 'r') as f:
                obj = json.load(f)
                for i in obj:
                    if i['en'] == en_label:
                        label = i['ja']
                        break
            
            #結果を表示
            mycamera.display_text(en_label + ":" + str(score))
            print(label + ":" + str(score))
            
            time.sleep(1)
            
    except:
        #映像プレビュー終了
        mycamera.stop_preview()
