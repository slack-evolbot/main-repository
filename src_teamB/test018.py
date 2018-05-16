#!/usr/bin/env python
# -*- coding: utf-8 -*-

#マイクからの入力を5秒間録音し、ファイル名：voice.wavで保存する。

import requests
import sys
sys.path.append("./talk_file/pyaudio/src/")
import pyaudio
import sys
import time
import wave

chunk = 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 1
#サンプリングレート、マイク性能に依存
RATE = 16000
#録音時間
RECORD_SECONDS = 5 #input('収録時間をしていしてください（秒数） >>>')

print('マイクに5秒間話しかけてください >>>')

#pyaudio
p = pyaudio.PyAudio()

#マイク0番を設定
input_device_index = 0
#マイクからデータ取得
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)
all = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
    data = stream.read(chunk)
    all.append(data)

stream.close()
data = ''.join(all)
out = wave.open('voice.wav','w')
out.setnchannels(1) #mono
out.setsampwidth(2) #16bit
out.setframerate(RATE)
out.writeframes(data)
out.close()

p.terminate()

print('<<< 録音完了')

path = '/home/pi/teamB/talk_file/voice.wav'
APIKEY = '664a7059443847546d446a6f3761526b386f4d424b425568657146664a32455a33417164644d4371437444'
url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)
files = {"a": open(path, 'rb'), "v":"on"}
r = requests.post(url, files=files)
print(r.json()['text'])
