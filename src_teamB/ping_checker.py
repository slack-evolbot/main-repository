import RPi.GPIO as GPIO
from time import sleep
import sys
import os
import pygame.mixer

hostname = "8.8.8.8"
LED_NORMAL = 22
LED_ERROR = 23

ping_counter = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_NORMAL, GPIO.OUT)
GPIO.setup(LED_ERROR, GPIO.OUT)

# ポート番号
SOUND_PORT = 17
# 周波数
TONES = {
    'ド': 523,
    'レ': 587,
    'ミ': 659,
    'ファ': 698,
    'ソ': 783,
    'ラ': 880,
    'シ': 987,
}

# メロディー
MELODY = ['ド', 'レ', 'ミ', 'ファ', 'ミ', 'レ', 'ド',
          'ミ', 'ファ', 'ソ', 'ラ', 'ソ', 'ファ', 'ミ']

# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PORT, GPIO.OUT)
# PWMを使う準備
pwm = GPIO.PWM(SOUND_PORT, 440)

# 音声ファイルの準備
pygame.mixer.init()
pygame.mixer.music.load("./g_string_quartet.mp3")

try:
    while True:
        response = os.system("ping -c 1 " + hostname)

        # PINGが通っている場合
        if response == 0:
            # 警告音を停止
            pygame.mixer.music.stop()
            # カウンタをリセット
            ping_counter = 0
            # 緑ランプをつける
            GPIO.output(LED_NORMAL, GPIO.HIGH)
            sleep(5)
        # PINGが通っていない場合
        else:
            # 連続３回通らなくなるまでカウンタを計上する
            if ping_counter < 3:
                ping_counter += 1

            # 連続３回通っていない場合はエラー処理を実行
            else:
                # 警告音を再生
                pygame.mixer.music.play(-1)
                # 緑ランプを消す
                GPIO.output(LED_NORMAL, GPIO.LOW)
                for mel in MELODY:
                    # 赤ランプをつける
                    GPIO.output(LED_ERROR, GPIO.HIGH)
                    # 周波数を設定
                    pwm.ChangeFrequency(TONES[mel])
                    # デューティー比50%で再生
                    pwm.start(50)
                    sleep(0.5)
                    # 赤ランプを消す
                    GPIO.output(LED_ERROR, GPIO.LOW)
                    # 停止
                    pwm.stop()
                    sleep(0.1)
                
except KeyboardInterrupt:
    # ランプを消し、警告音をオフにする
    GPIO.output(LED_ERROR, GPIO.LOW)
    GPIO.output(LED_NORMAL, GPIO.LOW)
    pygame.mixer.stop()
    pass

GPIO.clearnup()
sys.exit()
