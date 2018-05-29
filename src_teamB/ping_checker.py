import RPi.GPIO as GPIO
from time import sleep
import sys
import os
import pygame.mixer
import threading
import subprocess
import disp_util
import threading
import re

hostname = "8.8.8.8"
LED_NORMAL = 22
LED_ERROR = 23
BUTTON = 24

ping_counter = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_NORMAL, GPIO.OUT)
GPIO.setup(LED_ERROR, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

# tracerouteの結果
tr_text = []

# GPIOの設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PORT, GPIO.OUT)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# PWMを使う準備
pwm = GPIO.PWM(SOUND_PORT, 440)

# 音声ファイルの準備
pygame.mixer.init()
pygame.mixer.music.load("./g_string_quartet.mp3")

# ブザー音のフラグをTrueにする
switch_flg = True

def proc():
    bef_line = ''
    for line in tr_text:
        # IPアドレスが表示されていない場合
        if line.find("*") != -1:
            # IPアドレスを取得する
            m = re.search('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', bef_line)
            # ディスプレイに表示
            disp_util.print_disp("IP ADDRESS", m.group(0))
            break
        else:
            bef_line = line
try:
    while True:
        # PINGを実行し正常に動作しているか確認する
        ping_resp = subprocess.call("ping -c 1 " + hostname, shell=True)

        # PINGが通っている場合
        if ping_resp == 0:
            # ブザー音のフラグをTrueにする
            switch_flg = True
            # 警告音を停止
            pygame.mixer.music.stop()
	    # ディスプレイを初期化
            disp_util.print_disp("", "")
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
                # 緑ランプを消す
                GPIO.output(LED_NORMAL, GPIO.LOW)

                try:
		    # traceroute結果を取得する
                    response = subprocess.check_output("traceroute 8.8.8.8", universal_newlines=True, shell=True)
                    tr_text = str(response).split("\n")

                    # ディスプレイに表示
                    pt = threading.Thread(target=proc)
                    pt.start()

                except:
                    disp_util.print_disp("No Connect", "")

                for mel in MELODY:
                    # スイッチが押された場合、ブザー音のフラグをFalseに設定する
                    if GPIO.input(24) == GPIO.LOW:
                        switch_flg = False

                    # 赤ランプをつける
                    GPIO.output(LED_ERROR, GPIO.HIGH)

                    # スイッチが押されていない状態の場合
                    if switch_flg == True:
			# 警告音を再生
                        pygame.mixer.music.play(-1)
                        # 周波数を設定
                        pwm.ChangeFrequency(TONES[mel])
                        # デューティー比50%で再生
                        pwm.start(50)

                    # スイッチが押されている状態の場合
                    else:
                        # 警告音を停止
                        pygame.mixer.music.stop()

                    sleep(0.5)
                    # 赤ランプを消す
                    GPIO.output(LED_ERROR, GPIO.LOW)

                    # スイッチが押されていない状態の場合
                    if switch_flg == True:
                        # 停止
                        pwm.stop()

                    sleep(0.1)

except KeyboardInterrupt:
    # ランプを消し、警告音をオフにし、ディスプレイの文字を消す
    GPIO.output(LED_ERROR, GPIO.LOW)
    GPIO.output(LED_NORMAL, GPIO.LOW)
    pygame.mixer.stop()
    disp_util.print_disp("", "")
    pass

GPIO.cleanup()
sys.exit()

