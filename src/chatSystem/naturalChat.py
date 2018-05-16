# -*- coding: utf-8 -*-
import requests
import json
import types

def main(message, context, mode):
    KEY = '664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444'

    #エンドポイントの設定
    endpoint = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY=REGISTER_KEY'
    url = endpoint.replace('REGISTER_KEY', KEY)
    text = message.body['text']

    payload = {'utt' : text, 'context': context, 'mode': mode}
    headers = {'Content-type': 'application/json'}

    #送信
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()

    #jsonの解析
    resp_message = data['utt']
    resp_context = data['context']
    resp_mode = data['mode']

    #表示
    return resp_message, resp_context, resp_mode