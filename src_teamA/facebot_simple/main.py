# coding: utf-8
import RPi.GPIO as GPIO
import json
import my_camera
import time
import ms_api
import MySQLdb

SENSOR_GPIO = 5

#初期化
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_GPIO, GPIO.IN)

#定数定義
TEST_GROUP_NAME= "EvolvotGroup"
TEST_GROUP_ID = "evolvot_group"

#一時的写真ファイルパス
PHOTO_PATH = "./img/tmp.jpg"

mycamera = my_camera.MyCamera()
msapi = ms_api.MsApi()

class User():
    user_id = None
    user_name = None
    in_office = None
    
#person_idの人物を検索
def select_user_by_person_id(person_id):
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from evolcity_user where user_id = '" + person_id + "'"
    cursor.execute(sql)
    records = cursor.fetchall()
    
    #未登録であればNoneを返却
    if len(records) == 0:
        cursor.close()
        connector.close()
        return None
    
    #登録済みであればユーザ情報を返却
    user = User()
    user.user_id = records[0]["user_id"]
    user.user_name = records[0]["user_name"]
    user.in_office = records[0]["in_office"]
    cursor.close()
    connector.close()
    return user

if __name__ == "__main__":
    #映像プレビュー開始
    mycamera.start_preview()
    
    while True:
        if GPIO.input(SENSOR_GPIO) == GPIO.HIGH:
            mycamera.take_picture(PHOTO_PATH)
            #写真解析(写真上で一番大きな顔の人物）
            detect_results = msapi.detect_person(PHOTO_PATH)
            #顔が認識されない場合は再度ループ
            if detect_results == None or len(detect_results) == 0:
                continue

            mycamera.display_text(" Person Detected... ")
            
            #対象人物の候補を取得
            leargest_face_id = detect_results[0]["faceId"]
            identify_results = msapi.identify_person([leargest_face_id], TEST_GROUP_ID)
            candidate = msapi.get_most_candidate(identify_results)
            
            #confidenceが0.7未満の場合は再度ループ
            if candidate == None or candidate.confidence < 0.7:
                mycamera.display_text(" Sorry, I don't know you ")
                continue
            
            user = select_user_by_person_id(candidate.personId)
                
            #personIdが未登録の場合も再度ループ
            if user == None:
                mycamera.display_text(" Sorry, I don't know you ")
                continue
                
            #結果を表示
            mycamera.display_text(" Hello, " + user.user_name + "! ")            
            time.sleep(1)
