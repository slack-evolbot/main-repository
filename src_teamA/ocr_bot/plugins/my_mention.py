# coding: utf-8
import requests
import shutil
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import os
from vision import get_text_by_ms
import slackbot_settings

API_TOKEN = slackbot_settings.API_TOKEN

#アップロードされた画像を文字起こし
@listen_to("(.*)")
def img(message, params):
    #ファイル添付があった場合
    if 'file' in message.body:
        url = message.body['file']['url_private']
        flag = message.body['file']['filetype']
        tmpfile = "./tmp." + flag
        
        if(flag not in ["jpg","jpeg","png","gif"]):
            return

        message.send("文字起こし中…")
        
        #添付ファイルを一旦ローカルに保存
        rst = requests.get(url, headers={'Authorization': 'Bearer %s' % API_TOKEN}, stream=True)
        fo = open(tmpfile, "wb")
        shutil.copyfileobj(rst.raw, fo)
        fo.close()
        
        #API利用
        with open(tmpfile, 'rb') as f:
            data = f.read()
            
        message_text = get_text_by_ms(data)
        os.remove(tmpfile)
        message.send(message_text)