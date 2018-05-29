# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
from time import sleep
import MySQLdb
from datetime import datetime

#グループ毎のIDとGPIO
GROUP_ID_A = "A"
GROUP_ID_B = "B"
GROUP_ID_C = "C"
GROUP_ID_D = "D"
GPIO_A = 4
GPIO_B = 17
GPIO_C = 27
GPIO_D = 22
GPIO_START = 26

#ボタンステータス
STATUS_NORMAL = 0 #通常状態
STATUS_INPUT_SCORE = 1 #スコア入力待ち
STATUS_INPUT_CANCEL = 2 #キャンセル入力待ち
status = STATUS_NORMAL

#グループ情報格納用クラス
class Group():
    def __init__(self,group_id, group_name, score):
        self.group_id = group_id
        self.group_name = group_name
        self.score = score

#グループIDからグループ情報を取得
def get_score_by_group_id(group_id, connector):
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from score where group_id = '" + group_id + "'"
    cursor.execute(sql)
    record = cursor.fetchall()[0]
    cursor.close()
    group = Group(record["group_id"], record["group_name"], record["score"])
    
    return group

#グループID指定によるカウントアップ
def score_up_by_group_id(group_id, score, connector):
    cursor = connector.cursor()
    sql = "update score set score = " + str(score) + " where group_id = '" + group_id + "'"
    cursor.execute(sql)
    cursor.close()

#グループID指定によるスコア履歴追加
def insert_score_history_by_group_id(group_id, connector):
    cursor = connector.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into score_history(group_id, update_time) values('" + group_id + "', '" + now + "')"
    cursor.execute(sql)
    cursor.close()

#スコア全グループ取得
def get_score_all(connector):
    cursor = connector.cursor(MySQLdb.cursors.DictCursor)
    sql = "select * from score"
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    
    groups = []
    for record in records:
        group = Group(record["group_id"], record["group_name"], record["score"])
        groups.append(group)
        
    return groups

#スコアリセット
def reset_score(connector):
    cursor = connector.cursor()
    sql = "update score set score = 0"
    cursor.execute(sql)
    cursor.close()
    
    cursor = connector.cursor()
    sql = "delete from score_history"
    cursor.execute(sql)
    cursor.close()

#指定グループに1点加算
def score_up(group_id, connector):

    #現在の点数取得
    group = get_score_by_group_id(group_id, connector)
    
    #1点加算
    score = group.score + 1
    score_up_by_group_id(group_id, score, connector)
    
    #一応履歴も残す
    insert_score_history_by_group_id(group_id, connector)

#ボタン押下時のコールバック
def my_callback(channel):
    #DB接続
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    global status
    
    #キャンセル待ちの場合
    if status == STATUS_INPUT_CANCEL:
        if channel == GPIO_A:
            reset_score(connector)
            connector.commit()
            print("リセットしました")
        elif channel == GPIO_START:
            groups = get_score_all(connector)
            for group in groups:
              print(group.group_name + ":" + str(group.score))
        else:
            print("キャンセルしました")
        connector.close()
        #A以外ならキャンセル
        status = STATUS_NORMAL
        return
    
    #入力待ちの場合
    if status == STATUS_INPUT_SCORE:
        if channel == GPIO_A:
            score_up(GROUP_ID_A, connector)
        elif channel == GPIO_B:
            score_up(GROUP_ID_B, connector)
        elif channel == GPIO_C:
            score_up(GROUP_ID_C, connector)
        elif channel == GPIO_D:
            score_up(GROUP_ID_D, connector)
        else:
            print("リセット：A キャンセル：B 確認：M")
            status = STATUS_INPUT_CANCEL
            connector.close()
            return
            
        sleep(1)
        groups = get_score_all(connector)
        for group in groups:
            print(group.group_name + ":" + str(group.score))
        connector.commit()
        connector.close()
        print("投票ありがとうございました")
        status = STATUS_NORMAL
        return
        
    if channel == GPIO_START:
        status = STATUS_INPUT_SCORE
        print("投票してください")

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_C, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_D, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_START, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(GPIO_A, GPIO.BOTH, callback=my_callback, bouncetime=200)
GPIO.add_event_detect(GPIO_B, GPIO.BOTH, callback=my_callback, bouncetime=200)
GPIO.add_event_detect(GPIO_C, GPIO.BOTH, callback=my_callback, bouncetime=200)
GPIO.add_event_detect(GPIO_D, GPIO.BOTH, callback=my_callback, bouncetime=200)
GPIO.add_event_detect(GPIO_START, GPIO.BOTH, callback=my_callback, bouncetime=200)

try:
    while True:
        sleep(0.01)
        
except KeyboardInterrupt:
    pass

GPIO.cleanup()
