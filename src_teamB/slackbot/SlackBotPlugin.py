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
import naturalChat
import googlemaps
import datetime
import locale
import urllib.request
import shutil

from slacker import Slacker
from slackbot_settings import API_TOKEN

slacker = Slacker(API_TOKEN)

class TEMP_DATA():
    context_info = 'DUMMY'
    mode_info = 'dialog'

@listen_to(u'(おはようございます|しりとりしよう)')
@respond_to(u'(おはようございます|しりとりしよう)')
def resp_aplha(message, *something):
    lirc.init("test05", blocking = False)
    #chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], None, None)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = naturalChat.main(message, None, None)
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

@listen_to(u'(.*ランチ.*)')
@respond_to(u'(.*ランチ.*)')
def resp_lunch(message, *something):
    now_place = '東京都新宿区西新宿1-21-1 明宝ビル'
    google_map_key = 'AIzaSyCuxTpu4wHcCz1M9S3GNLMfbCYmrc-b-dg'

    connection = MySQLdb.connect(host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')

    today = datetime.date.today()
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        
    try:
        with connection.cursor() as cursor:
            pattern = r".*おすすめ.*"
            repatter = re.compile(pattern)

            if repatter.match(message.body['text']):
                sql = "SELECT SHOP_NAME, SPECIAL FROM SERVICE_LUNCH_TABLE WHERE SERVICE_DAY = '" + str(today.day) + "' OR SERVICE_WEEK = '" + today.strftime('%a') + "';"            
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()

                if len(result) == 0:
                    sql = "SELECT SHOP_NAME, DETAIL FROM RECOMMENDED_LUNCH_TABLE WHERE RANK >= 5;"            
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    cursor.close()

                    ran = random.randint(0, len(result)-1)
                    shop_name = result[ran][0]
                    special = result[ran][1]
                elif len(result) >= 2:
                    ran = random.randint(0, len(result)-1)
                    shop_name = result[ran][0]
                    special = result[ran][1]
                else:
                    shop_name = result[0][0]
                    special = result[0][1]
            else:
                pattern = r".*チャレンジ.*"
                repatter = re.compile(pattern)

                if repatter.match(message.body['text']):
                    sql = "SELECT SHOP_NAME, DETAIL FROM RECOMMENDED_LUNCH_TABLE WHERE RANK = -1;"            
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    cursor.close()

                    ran = random.randint(0, len(result)-1)
                    shop_name = result[ran][0]
                    special = result[ran][1]

                else:
                    sql = "SELECT SHOP_NAME, DETAIL FROM RECOMMENDED_LUNCH_TABLE WHERE RANK >= 5;"            
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    cursor.close()

                    ran = random.randint(0, len(result)-1)
                    shop_name = result[ran][0]
                    special = result[ran][1]

            gmaps = googlemaps.Client(key=google_map_key)

            directions_result = gmaps.directions(now_place, "新宿 " + shop_name, mode="walking", alternatives=False, language="ja")

            message.send("今日のおすすめは" + shop_name + "です")
            message.send(shop_name + "は" + special)
            
            message.send(shop_name + "まで" + re.sub(" ", "", directions_result[0]['legs'][0]['distance']['text']) + "(" + directions_result[0]['legs'][0]['duration']['text'] + ")")
            #create_map_image(shop_name)
            lat = str(directions_result[0]['legs'][0]['end_location']['lat'])
            lng = str(directions_result[0]['legs'][0]['end_location']['lng'])
            #url = "http://maps.google.com/maps/api/staticmap?center=" + lat + "," + lng + "&zoom=18&size=640x480&markers=" + lat + "%2C" + lng + "&sensor=false&key=" + google_map_key;
            url="https://maps.googleapis.com/maps/api/staticmap?path=weight%3A10%7Ccolor%3Ared"

            message.send(now_place + 'からの道順は下記です')
            counter = 1
            for step in directions_result[0]['legs'][0]['steps']:
                url +=  "%7C" + str(step['start_location']['lat']) + "%2C" + str(step['start_location']['lng'])
                message.send('{0:02d}'.format(counter) + ". " + re.sub(" ", "", step['distance']['text']) + re.sub(r'[\x20-\x7E]+', "", re.sub("<div", "（", re.sub("</div>", "）", step['html_instructions']))))
                counter += 1

            url += "%7C" + lat + "%2C" + lng + "&markers=" + lat + "%2C" + lng + "&size=640x480&key=" + google_map_key

            download_pic(url, shop_name)

            shutil.copy("/home/pi/teamB/map/" + str(shop_name) + ".png", "/home/pi/teamB/map/upload_file.png")
            slacker.files.upload("/home/pi/teamB/map/upload_file.png" , filename="upload_file.png", channels=message.body['channel'])
            os.remove("/home/pi/teamB/map/upload_file.png")

    except Exception as e:
        print("{0}".format(e))
    

@listen_to(u'(^(?!(おはようございます|しりとりしよう|.*？|勤務表参照|勤怠.*|.*ランチ.*)).+$)')
@respond_to(u'(^(?!(おはようございます|しりとりしよう|.*？|勤務表参照|勤怠.*|.*ランチ.*)).+$)')
def resp_beta(message, *something):
    lirc.init("test05", blocking = False)
    #chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = chat.main(message.body['text'], TEMP_DATA.context_info, TEMP_DATA.mode_info)
    chat_message, TEMP_DATA.context_info, TEMP_DATA.mode_info = naturalChat.main(message, TEMP_DATA.context_info, TEMP_DATA.mode_info)
    print(message.body['text'])
    message.send(chat_message)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi "' + chat_message + '" | aplay', shell=True)

def download_pic(url,filename):
    img = urllib.request.urlopen(url)
    localfile = open( "/home/pi/teamB/map/" + str(filename) + ".png" , 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()
