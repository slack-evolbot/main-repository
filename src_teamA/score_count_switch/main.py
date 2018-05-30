# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
from time import sleep
import MySQLdb
from datetime import datetime
import display

#ディスプレイ表示用
disp = display.Display()

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
STATUS_WAITING = 0 #入力なし状態
STATUS_NORMAL = 1 #通常状態
STATUS_INPUT_SCORE = 2 #スコア入力中
STATUS_INPUT_RESET = 3 #リセット入力中
status = STATUS_WAITING

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
    return score

def show_score(groups):
    display_message1 = " " + groups[0].group_name + "   " + groups[1].group_name + "   " + groups[2].group_name + "   " + groups[3].group_name
    display_message2 = '{0:03d}'.format(groups[0].score) + " " + '{0:03d}'.format(groups[1].score) + " " + '{0:03d}'.format(groups[2].score) + " " + '{0:03d}'.format(groups[3].score)
    print(display_message1)
    print(display_message2)
    disp.lcd_string1and2(display_message1, display_message2)

#ボタン押下時のコールバック
def my_callback(channel):
    #DB接続
    connector = MySQLdb.connect(host="localhost", db="raspberry", user="pi", passwd="k-evolva", charset="utf8")
    global status
    
    if status == STATUS_WAITING:
        print(channel)
        #最初はどのボタンを押されても点数表示
        groups = get_score_all(connector)
        show_score(groups)
        status = STATUS_NORMAL
    elif status == STATUS_INPUT_RESET:
         #リセット待ちの場合
        if channel == GPIO_A:
            reset_score(connector)
            connector.commit()
            disp.lcd_string1("Reset Complete!!")
            print("リセットしました")
        else:
            disp.lcd_string1("Calceled")
            print("キャンセルしました")
        sleep(2)
        status = STATUS_NORMAL
        groups = get_score_all(connector)
        show_score(groups)
    elif status == STATUS_INPUT_SCORE:
        #入力待ちの場合
        if channel == GPIO_A:
            score = score_up(GROUP_ID_A, connector)
            connector.commit()
            disp.lcd_string1and2(GROUP_ID_A + " Selected!!", "Score: " + '{0:03d}'.format(score))
        elif channel == GPIO_B:
            score = score_up(GROUP_ID_B, connector)
            connector.commit()
            disp.lcd_string1and2(GROUP_ID_B + " Selected!!", "Score: " + '{0:03d}'.format(score))
        elif channel == GPIO_C:
            score = score_up(GROUP_ID_C, connector)
            connector.commit()
            disp.lcd_string1and2(GROUP_ID_C + " Selected!!", "Score: " + '{0:03d}'.format(score))
        elif channel == GPIO_D:
            score = score_up(GROUP_ID_D, connector)
            connector.commit()
            disp.lcd_string1and2(GROUP_ID_D + " Selected!!", "Score: " + '{0:03d}'.format(score))
        else:
            disp.lcd_string1and2("Reset : A", "Cancel: Others")
            print("リセット：A キャンセル")
            status = STATUS_INPUT_RESET
            connector.close()
            return
            
        sleep(2)
        disp.lcd_string1("Thank you!!")
        print("投票ありがとうございました")
        sleep(2)
        status = STATUS_NORMAL
        groups = get_score_all(connector)
        show_score(groups)
    elif status == STATUS_NORMAL:
        if channel == GPIO_START:
            status = STATUS_INPUT_SCORE
            disp.lcd_string1("Input button!!")
            print("投票してください")
    connector.close()

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_A, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_B, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_C, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_D, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(GPIO_START, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(GPIO_A, GPIO.FALLING, callback=my_callback, bouncetime=500)
GPIO.add_event_detect(GPIO_B, GPIO.FALLING, callback=my_callback, bouncetime=500)
GPIO.add_event_detect(GPIO_C, GPIO.FALLING, callback=my_callback, bouncetime=500)
GPIO.add_event_detect(GPIO_D, GPIO.FALLING, callback=my_callback, bouncetime=500)
GPIO.add_event_detect(GPIO_START, GPIO.FALLING, callback=my_callback, bouncetime=500)

try:
    while True:
        sleep(0.01)
        
except KeyboardInterrupt:
    pass
finally:
    disp.end_display()
    GPIO.cleanup()

