# coding: utf-8
import requests
import shutil
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import time
import os
import json

LABEL_JSON_PATH = './label.json'
SLEEP_TIME = 1

@listen_to("(.*)")
def img(message, params):
    
    if 'file' in message.body:
        url = message.body['file']['url_private']
        flag = message.body['file']['filetype']
        tmpfile = "./tmp." + flag
        
        if(flag not in ["jpg","jpeg","png","gif"]):
            return

        token = 'xoxb-360090495013-8npN9mSma8EjIP3XuxRuuH7U'
        rst = requests.get(url, headers={'Authorization': 'Bearer %s' % token}, stream=True)

        fo = open(tmpfile, "wb")
        shutil.copyfileobj(rst.raw, fo)
        fo.close()
        
        message.send("画像解析中…")
        
        for i in range(10):
            if(os.path.exists(LABEL_JSON_PATH)):
                f = open(LABEL_JSON_PATH, 'r')
                json_data = json.load(f)
                
                score = float(json_data["score"])
                label = json_data["label"]
                
                if(score >= 0.7):
                    message_str = "「" + label + "」だね。間違いない！"
                elif(score >= 0.5 and score < 0.7):
                    message_str = "「" + label + "」だと思うよ。"
                elif(score >= 0.3 and score < 0.5):
                    message_str = "「" + label + "」かな。たぶん。"
                elif(score < 0.3):
                    message_str = "「" + label + "」かも…？自信ないけど。"
                    
                message.send(message_str)
                os.remove(LABEL_JSON_PATH)
                os.remove(tmpfile)
                break
            time.sleep(SLEEP_TIME)

