# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
import time
import os
import ms_api
import my_camera
import MySQLdb
from datetime import datetime
import sys
import pygame.mixer

#定数定義
SLEEP_TIME = 1
SENSOR_GPIO = 5
CAPTURE_IMAGE_PATH = './img/face.jpg'
TEST_GROUP_NAME= "EvolvotGroup"
TEST_GROUP_ID = "evolvot_group"

#初期化
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_GPIO, GPIO.IN)

#インスタンス生成
mycamera = my_camera.MyCamera()
msapi = ms_api.MsApi()
pygame.mixer.init()
camera_sound = pygame.mixer.Sound("./sound/camera.wav")
ok_sound = pygame.mixer.Sound("./sound/ok.wav")
ng_sound = pygame.mixer.Sound("./sound/ng.wav")

class User():
    user_id = None
    user_name = None
    in_office = None

#person_idの人物を登録
def register_person(person_id, person_name):
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor()
    sql = "insert into evolcity_user(user_id, user_name, in_office) values('" + person_id + "', '" + person_name + "', 0)"
    cursor.execute(sql)
    cursor.close()
    connector.commit()
    connector.close()
    print("ユーザDB登録完了")

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

#user_idの人物の出勤情報を登録
def register_inout(user):
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor()
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    sql = "select * from evolcity_inout_history where user_id = '" + user.user_id + "' and date = '" + today + "'"
    cursor.execute(sql)
    records = cursor.fetchall()

    #本日の出勤情報が未登録であれば新規登録
    if len(records) == 0:
        sql = "insert into evolcity_inout_history(user_id, date, in_time, out_time) values('" + user.user_id + "', '" + today + "', '" + time + "', null)"
        cursor.execute(sql)
    else:
        #登録済みであれば、outする場合のみ更新
        if user.in_office == 1:
            sql = "update evolcity_inout_history set out_time = '" + time + "' where user_id = '" + user.user_id + "'"
            cursor.execute(sql)
    
    #ユーザーのinout状態を更新
    update_in_office = 0
    if user.in_office == 0:
        update_in_office = 1
    sql = "update evolcity_user set in_office = " + str(update_in_office) + " where user_id = '" + user.user_id + "'"
    cursor.execute(sql)
    cursor.close()
    connector.commit()
    connector.close()

#人物作成とトレーニング
def create_and_training(person_name, group_id):
    data = msapi.create_person(person_name, group_id)
    person_id = data["personId"]
    mycamera.take_pictures("./training_img/", 260) #max248だが予備のため260
    msapi.add_person_photo(group_id, person_id)
    msapi.train(group_id)
    msapi.get_training_status(group_id)
    register_person(person_id, person_name)

#人物写真追加
def add_person_photo(group_id, person_id, count):
    mycamera.take_pictures("./training_img/", count)
    msapi.add_person_photo(group_id, person_id)
    msapi.train(group_id)
    msapi.get_training_status(group_id)

#全ユーザ取得
def get_all_users():
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from evolcity_user"
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    connector.close()
    
    users = []
    for record in records:
        user = User()
        user.user_id = record["user_id"]
        user.user_name = record["user_name"]
        user.in_office = record["in_office"]
        users.append(user)
        print(vars(user))
    return users

#社内にいるユーザ取得
def get_in_users():
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from evolcity_user where in_office = 1"
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    connector.close()
    
    users = []
    for record in records:
        user = User()
        user.user_id = record["user_id"]
        user.user_name = record["user_name"]
        user.in_office = record["in_office"]
        users.append(user)
        print(vars(user))
    return users

#指定IDのユーザの状態取得
def get_user_by_id(user_id):
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from evolcity_user where user_id = '" + user_id + "'"
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    connector.close()
    
    #未登録であればNoneを返却
    if len(records) == 0:
        cursor.close()
        connector.close()
        return None
    
    user = User()
    user.user_id = records[0]["user_id"]
    user.user_name = records[0]["user_name"]
    user.in_office = records[0]["in_office"]
    print(vars(user))
        
    return user
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        while True:
            print("...")
            if GPIO.input(SENSOR_GPIO) == GPIO.HIGH:
                
                #写真撮影
                print("動作を検知しました。撮影します。")
                camera_sound.play()
                mycamera.take_picture(CAPTURE_IMAGE_PATH)
                
                #写真解析(写真上で一番大きな顔の人物）
                detect_results = msapi.detect_person(CAPTURE_IMAGE_PATH)
                #顔が認識されない場合は再度ループ
                if detect_results == None or len(detect_results) == 0:
                    ng_sound.play()
                    print("顔が認識できませんでした。")
                    continue
                
                #対象人物の候補を取得
                leargest_face_id = detect_results[0]["faceId"]
                identify_results = msapi.identify_person([leargest_face_id], TEST_GROUP_ID)
                candidate = msapi.get_most_candidate(identify_results)
                
                #confidenceが0.7未満の場合は再度ループ
                if candidate == None or candidate.confidence < 0.7:
                    ng_sound.play()
                    print("未登録の顔です。")
                    continue
                
                user = select_user_by_person_id(candidate.personId)
                
                #personIdが未登録の場合も再度ループ
                if user == None:
                    ng_sound.play()
                    print("未登録の顔です。")
                    continue

                #出勤/退勤と状態を更新
                ok_sound.play()
                register_inout(user)
                print("こんにちは！" + user.user_name + "さん")
                    
            time.sleep(SLEEP_TIME)

    args = sys.argv
    if args[1] == "in":
        get_in_users()
    elif args[1] == "all":
        get_all_users()
    elif args[1] == "id":
        user_id = input('UserId >> ')
        get_user_by_id(user_id)
    elif args[1] == "newuser":
        user_name = input('New UserName >> ')
        create_and_training(user_name, TEST_GROUP_ID)
    elif args[1] == "deluser":
        user_id = input('Del UserId >> ')
        msapi.delete_person(user_id, TEST_GROUP_ID)
    elif args[1] == "addphoto":
        user_id = input('UserId >> ')
        count = input('Photo Number >> ')
        add_person_photo(TEST_GROUP_ID, user_id, int(count))
    elif args[1] == "newgroup":
        msapi.create_group(TEST_GROUP_NAME, TEST_GROUP_ID)
