# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
from requests.exceptions import RequestException
from plugins.gnaviapi import GnaviApi
import urllib.request
import json
import MySQLdb
import time
import lirc
import random
import sys
sys.path.append("../")
import disp_test01
import os
sys.path.append("../chatSystem/")
import chat

# チャンネル１に変更
@listen_to(u'(チャンネル1|チャンネル１|ch1)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル1|チャンネル１|ch1)+.*(変え|かえ)+.*')
def ch1Change(message, *something):
    # チャンネルを１に変更する :
    message.reply(u'チャンネルを１に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("1")

# チャンネル２に変更
@listen_to(u'(チャンネル2|チャンネル２|ch2)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル2|チャンネル２|ch2)+.*(変え|かえ)+.*')
def ch2Change(message, *something):
    # チャンネルを２に変更する :
    message.reply(u'チャンネルを２に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("2")

# チャンネル３に変更
@listen_to(u'(チャンネル3|チャンネル３|ch3)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル3|チャンネル３|ch3)+.*(変え|かえ)+.*')
def ch3Change(message, *something):
    # チャンネルを３に変更する :
    message.reply(u'チャンネルを３に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("3")

# チャンネル４に変更
@listen_to(u'(チャンネル4|チャンネル４|ch4)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル4|チャンネル４|ch4)+.*(変え|かえ)+.*')
def ch4Change(message, *something):
    # チャンネルを４に変更する :
    message.reply(u'チャンネルを４に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("4")

# チャンネル５に変更
@listen_to(u'(チャンネル5|チャンネル５|ch5)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル5|チャンネル５|ch5)+.*(変え|かえ)+.*')
def ch5Change(message, *something):
    # チャンネルを５に変更する :
    message.reply(u'チャンネルを５に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("5")

# チャンネル６に変更
@listen_to(u'(チャンネル6|チャンネル６|ch6)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル6|チャンネル６|ch6)+.*(変え|かえ)+.*')
def ch6Change(message, *something):
    # チャンネルを６に変更する :
    message.reply(u'チャンネルを６に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("6")

# チャンネル７に変更
@listen_to(u'(チャンネル7|チャンネル７|ch7)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル7|チャンネル７|ch7)+.*(変え|かえ)+.*')
def ch7Change(message, *something):
    # チャンネルを７に変更する :
    message.reply(u'チャンネルを７に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("7")

# チャンネル８に変更
@listen_to(u'(チャンネル8|チャンネル８|ch8)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル8|チャンネル８|ch8)+.*(変え|かえ)+.*')
def ch8Change(message, *something):
    # チャンネルを８に変更する :
    message.reply(u'チャンネルを８に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("8")

# チャンネル９に変更
@listen_to(u'(チャンネル9|チャンネル９|ch9)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル9|チャンネル９|ch9)+.*(変え|かえ)+.*')
def ch9Change(message, *something):
    # チャンネルを９に変更する :
    message.reply(u'チャンネルを９に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("9")

# チャンネル０に変更
@listen_to(u'(チャンネル0|チャンネル０|ch0)+.*(変え|かえ)+.*')
@respond_to(u'(チャンネル0|チャンネル０|ch0)+.*(変え|かえ)+.*')
def ch0Change(message, *something):
    # チャンネルを０に変更する :
    message.reply(u'チャンネルを０に変更します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("0")

# 温度
@listen_to(u'(温度|おんど|temperature)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
@respond_to(u'(温度|おんど|temperature)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
def temperatureDisp(message, *something):
    # 温度を表示する :
    message.reply(u'温度を表示します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("3")

# 湿度
@listen_to(u'(湿度|しつど|humidity)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
@respond_to(u'(湿度|しつど|humidity)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
def temperatureDisp(message, *something):
    # 温度を表示する :
    message.reply(u'湿度を表示します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("4")

# 気圧
@listen_to(u'(気圧|きあつ|atmospheric|pressure)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
@respond_to(u'(気圧|きあつ|atmospheric|pressure)+.*(教え|おし|見|みたい|みせて|知|しりたい)+.*')
def temperatureDisp(message, *something):
    # 温度を表示する :
    message.reply(u'気圧を表示します。')
    file = open('/home/pi/teamB/SLACK_BOT_CH_NO.txt', 'w')  #書き込みモードでオープン
    file.write("5")

@listen_to(u'(ご飯|ごはん)+.*')
@respond_to(u'(ご飯|ごはん)+.*')
def search_restraunt(message, *something):

    """
        受信メッセージを元にぐるなびを検索してURLを返す
    """
    gnavi = GnaviApi('https://api.gnavi.co.jp/RestSearchAPI/20150630/')
    key = '84496dd02f5456f1cfaf3fa412621a77'

    search_word = message.body['text'].split()

    if len(search_word) == 3:
        params = {
            'keyid': key,
            'format': 'json',
            'address': search_word[1],
            'freeword': search_word[2]
        }

        try:
            gnavi.api_request(params)
            for rest_url in gnavi.url_list():
                message.send(rest_url)
        except RequestException:
            message.send('ぐるなびに繋がりません。時間をおいて再度検索してください。')
            return
        except Exception as other:
            message.send(''.join(other.args))
            return
    else:
        message.send('↓こんな感じで検索してほしい・・・(￣Д￣)ﾉ')
        message.send('ご飯　場所　キーワード（文字はスペース区切り）')
        message.send('例）ご飯　品川　焼き鳥')

@listen_to(u'(天気|てんき|weather)+.*')
@respond_to(u'(天気|てんき|weather)+.*')
def get_weather_api(message, *something):

    search_city_name = message.body['text'].split()[1]

    connection = MySQLdb.connect(
    host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT CITY_CODE FROM CITY_CODE_TABLE WHERE CITY_NAME ='"+search_city_name+"'"
            cursor.execute(sql)
            result = cursor.fetchall()

        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='+result[0][0]
        html = urllib.request.urlopen(url)
        resp = json.loads(html.read().decode('utf-8'))

        returnMessage = '**************************' + '\n'
        returnMessage += resp['title']+'\n'
        returnMessage += '**************************'+'\n'
        returnMessage += resp['description']['text']+'\n'

        for forecast in resp['forecasts']:
            returnMessage += '**************************'+'\n'
            returnMessage += forecast['dateLabel']+'('+forecast['date']+')'+'\n'
            returnMessage += forecast['telop']+'\n'
            returnMessage += '**************************'+'\n'
        message.send(returnMessage)

    except:
        message.send('↓こんな感じで検索してほしい・・・(￣Д￣)ﾉ')
        message.send('天気　場所（文字はスペース区切り）')

@listen_to(u'(しりとり)+.*')
@respond_to(u'(しりとり)+.*')
def get_weather_api(message, *something):

    search_word= message.body['text'].split()[1]

    connection = MySQLdb.connect(
    host='localhost', user='pi', passwd='pass', db='raspberry', charset='utf8')
    
    try:
        with connection.cursor() as cursor:
            sql = " SELECT ALL_WORD FROM WORD_MASTER WHERE CONVERT (TOP_WORD using utf8) collate utf8_unicode_ci like RIGHT('"+search_word+"',1) and USED_FLAG = '0' LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchall()

        return_word = result[0][0]

        message.send(return_word)

        with connection.cursor() as cursor:
            sql = "UPDATE WORD_MASTER SET USE_FLG = '1' WHERE ALL_WORD = '" + return_word + "'"
            cursor.execute(sql)
            result = cursor.fetchall()

    except:
        print("予期せぬ例外が発生しました。")

@listen_to(u'(暗算ゲーム|あんざんゲーム)+.*(初心者|しょしんしゃ)+.*')
@respond_to(u'(暗算ゲーム|あんざんゲーム)+.*(初心者|しょしんしゃ)+.*')
def cluc_game(message, *something):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    disp_test01.print_disp("READY?","LEVEL 0")

    while True:
        codeIR = lirc.nextcode()
        if(codeIR != [] and codeIR[0] == "PLAY"):
            disp_test01.print_disp("GAME START!","")
            lirc.deinit()
            time.sleep(1)
            total_Number = 0
            for i in range(7):
                disp_Number = random.randint(1,9)
                total_Number = total_Number + disp_Number
                disp_test01.print_disp(str(disp_Number),"")
                time.sleep(0.8)
                disp_test01.print_disp("","")
            disp_test01.print_disp("","")                
            file = open('/home/pi/teamB/SLACK_BOT_QUIZ.txt', 'w')  #書き込みモードでオープン
            file.write(str(total_Number))
            message.send("答えを入力してください")
            break
                
        else:
            time.sleep(3)
            
@listen_to(u'(暗算ゲーム|あんざんゲーム)+.*(初級|簡単|かんたん)+.*')
@respond_to(u'(暗算ゲーム|あんざんゲーム)+.*(初級|簡単|かんたん)+.*')
def cluc_game(message, *something):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    disp_test01.print_disp("READY?","LEVEL 1")

    while True:
        codeIR = lirc.nextcode()
        if(codeIR != [] and codeIR[0] == "PLAY"):
            disp_test01.print_disp("GAME START!","")
            lirc.deinit()
            time.sleep(1)
            total_Number = 0
            for i in range(3):
                disp_Number = random.randint(1,30)
                total_Number = total_Number + disp_Number
                disp_test01.print_disp(str(disp_Number),"")
                time.sleep(1.2)
            disp_test01.print_disp("","")                
            file = open('/home/pi/teamB/SLACK_BOT_QUIZ.txt', 'w')  #書き込みモードでオープン
            file.write(str(total_Number))
            message.send("答えを入力してください")
            break
                
        else:
            time.sleep(3)

@listen_to(u'(暗算ゲーム|あんざんゲーム)+.*(中級|ふつう)+.*')
@respond_to(u'(暗算ゲーム|あんざんゲーム)+.*(中級|ふつう)+.*')
def cluc_game(message, *something):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    disp_test01.print_disp("READY?","LEVEL 2")

    while True:
        codeIR = lirc.nextcode()
        if(codeIR != [] and codeIR[0] == "PLAY"):
            disp_test01.print_disp("GAME START!","")
            lirc.deinit()
            time.sleep(1)
            total_Number = 0
            for i in range(5):
                disp_Number = random.randint(1,100)
                total_Number = total_Number + disp_Number
                disp_test01.print_disp(str(disp_Number),"")
                time.sleep(1)
            disp_test01.print_disp("","")                
            file = open('/home/pi/teamB/SLACK_BOT_QUIZ.txt', 'w')  #書き込みモードでオープン
            file.write(str(total_Number))
            message.send("答えを入力してください")
            break
                
        else:
            time.sleep(3)

@listen_to(u'(暗算ゲーム|あんざんゲーム)+.*(上級|難|むず)+.*')
@respond_to(u'(暗算ゲーム|あんざんゲーム)+.*(上級|難|むず)+.*')
def cluc_game(message, *something):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    disp_test01.print_disp("READY?","LEVEL 3")

    while True:
        codeIR = lirc.nextcode()
        if(codeIR != [] and codeIR[0] == "PLAY"):
            disp_test01.print_disp("GAME START!","")
            lirc.deinit()
            time.sleep(1)
            total_Number = 0
            for i in range(8):
                disp_Number = random.randint(1,100)
                total_Number = total_Number + disp_Number
                disp_test01.print_disp(str(disp_Number),"")
                time.sleep(0.7)
            disp_test01.print_disp("","")                
            file = open('/home/pi/teamB/SLACK_BOT_QUIZ.txt', 'w')  #書き込みモードでオープン
            file.write(str(total_Number))
            message.send("答えを入力してください")
            break
                
        else:
            time.sleep(3)

@listen_to(u'(お話しましょう|おはなししましょう)+.*')
@respond_to(u'(お話しましょう|おはなししましょう)+.*')
def cluc_game(message, *something):

    #Initialize lirc
    lirc.init("test05", blocking = False)
    chat.main()

    while True:
        if(str(message.body['text']) == 'お話終わり'):
            break
    else:
#        resp = chat.send_and_get(message)
        resp = chat.send_and_get(str(message.body['text']))
#        print('Enemy  : %s'%(resp))
        message.send('Enemy  : %s'%(resp))


@listen_to(u'[0-9]+')
@respond_to(u'[0-9]+')
def cluc_game_anser(message, *something):
    #message.send(str(1)+":"+str(message.body['text']))
    #message.send(str(toral_Number)+":"+str(message.body['text']))
    if(os.path.exists("/home/pi/teamB/SLACK_BOT_QUIZ.txt")):
        file = open("/home/pi/teamB/SLACK_BOT_QUIZ.txt")
        total_Number = file.readline().replace('\r|\n|\r\n',"")
        if(str(message.body['text']) == str(total_Number)):
            message.send("正解")
            os.remove("/home/pi/teamB/SLACK_BOT_QUIZ.txt")
        else:
            message.send("/poll\"ぶっぶー もう1回やる？\" \"YES\" \"NO\"")
            message.send("正解は「"+str(total_Number)+"」")
            message.send("GAME OVER...")
            os.remove("/home/pi/teamB/SLACK_BOT_QUIZ.txt")
