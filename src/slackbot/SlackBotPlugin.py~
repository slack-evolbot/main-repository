# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
from requests.exceptions import RequestException
import json
import time
import lirc
import random
import sys
sys.path.append("../")
import disp_test01
import os
sys.path.append("../chatSystem/")
import chat
import qaChat
import subprocess
import MySQLdb
from texttable import Texttable

class TEMP_DATA():
    context_info = 'DUMMY'
    mode_info = 'dialog'

@listen_to(u'(おはようございます|しりとりしよう)')
@respond_to(u'(おはようございます|しりとりしよう)')
def resp_aplha(message, *something):
    lirc.init("test05", blocking = False)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], None, None)
    print(message.body['text'])
    message.send(chat_message)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi "' + chat_message + '" | aplay', shell=True)    

@listen_to(u'(.*？)')
@respond_to(u'(.*？)')
def resp_gamma(message, *something):
    lirc.init("test05", blocking = False)
    chat_message = qaChat.main(message.body['text'])
    print(message.body['text'])
    message.send(chat_message)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi "' + chat_message + '" | aplay', shell=True)

@listen_to(u'(勤務表参照)')
@respond_to(u'(勤務表参照)')
def resp_delta(message, *something):
    connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT KINMU_YMD,SYUSSYA_TIME,TAISYA_TIME FROM KINTAI_TABLE INNER JOIN SLACK_ID_TABLE ON KINTAI_TABLE.SYAIN_CD = SLACK_ID_TABLE.SYAIN_CD WHERE SLACK_ID_TABLE.SLACK_ID = '" + message.body['user'] + "';"
            
            cursor.execute(sql)
            result = cursor.fetchall()

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_align(["l", "l", "l"])
            table.set_cols_width([20, 20, 20])
            table.header(['勤務日', '出社時間', '退勤時間'])
            table.add_rows(result, False)

            message.reply('')
            message.send(table.draw())

    except:
        message.send('例外が発生しました')

@listen_to(u'(勤怠|きんたい)+.*(出勤|出社|しゅっきん|しゅっしゃ|退勤|退社|たいきん|たいしゃ)+.*')
@respond_to(u'(勤怠|きんたい)+.*(出勤|出社|しゅっきん|しゅっしゃ|退勤|退社|たいきん|たいしゃ)+.*')
def resp_kintai(message, *something):
    kbn = message.body['text'].split()[1]
    slackId = message.body['user'];

    connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')

    try:
        if(kbn == '出勤' or kbn == '出社' or kbn == 'しゅっきん' or kbn == 'しゅっしゃ'):
            with connection.cursor() as cursor:
                sql = "UPDATE raspberry.KINTAI_TABLE A"
                sql += " LEFT JOIN raspberry.SLACK_ID_TABLE B"
                sql += " ON B.SLACK_ID = '" + slackId + "'"
                sql += " SET A.SYUSSYA_TIME = date_format(now(), '%H:%i')"
                sql += " WHERE A.SYAIN_CD = B.SYAIN_CD"
                sql += " AND A.KINMU_YMD = date_format(now(), '%Y-%m-%d');"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                message.send("出勤しました")
        elif(kbn == '退勤' or kbn == '退社' or kbn == 'たいきん' or kbn == 'たいしゃ'):
            with connection.cursor() as cursor:
                sql = "UPDATE raspberry.KINTAI_TABLE A"
                sql += " LEFT JOIN raspberry.SLACK_ID_TABLE B"
                sql += " ON B.SLACK_ID = '" + slackId + "'"
                sql += " SET A.TAISYA_TIME = date_format(now(), '%H:%i')"
                sql += " WHERE A.SYAIN_CD = B.SYAIN_CD"
                sql += " AND A.KINMU_YMD = date_format(now(), '%Y-%m-%d');"
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                message.send("退勤しました")
        else:
            message.send("↓こんな感じで検索してほしい・・・(￣Д￣)ﾉ")
            message.send("勤怠 出勤or退勤")
    except:
        connection.rollback()
        message.send("↓こんな感じで検索してほしい・・・(￣Д￣)ﾉ")
        message.send("勤怠 出勤or退勤")
    finally:
        cursor.close()
        connection.close()

@listen_to(u'(^(?!(おはようございます|しりとりしよう|.*？|勤務表参照|勤怠.*)).+$)')
@respond_to(u'(^(?!(おはようございます|しりとりしよう|.*？|勤務表参照|勤怠.*)).+$)')
def resp_beta(message, *something):
    lirc.init("test05", blocking = False)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], TEMP_DATA.context_info, TEMP_DATA.mode_info)
    print(message.body['text'])
    message.send(chat_message)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi "' + chat_message + '" | aplay', shell=True)

    
