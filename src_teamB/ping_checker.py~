import RPi.GPIO as GPIO
from time import sleep
import sys
import os

hostname = "192.168.20.254"
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

try:
    while True:
        response = os.system("ping -c 1 " + hostname)

        if response == 0:
            ping_counter = 0
            GPIO.output(LED_ERROR, GPIO.LOW)
            GPIO.output(LED_NORMAL, GPIO.HIGH)
            sleep(5)
        else:
            if ping_counter < 3:
                ping_counter += 1
            else:
                GPIO.output(LED_NORMAL, GPIO.LOW)
                for mel in MELODY:
                    GPIO.output(LED_ERROR, GPIO.HIGH)
                    # 周波数を設定
                    pwm.ChangeFrequency(TONES[mel])
                    # デューティー比50%で再生
                    pwm.start(50)
                    sleep(0.5)
                    GPIO.output(LED_ERROR, GPIO.LOW)
                    # 停止
                    pwm.stop()
                    sleep(0.1)
                
except KeyboardInterrupt:
    GPIO.output(LED_ERROR, GPIO.LOW)
    GPIO.output(LED_NORMAL, GPIO.LOW)
    pass

GPIO.clearnup()
sys.exit()
