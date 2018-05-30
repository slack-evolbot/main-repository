# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
import time
import datetime
import pygame.mixer
import my_camera
from datetime import datetime

#定数定義
SLEEP_TIME = 1
SENSOR_GPIO = 5
SENSOR_WAIT_TIME = 4
CAMERA_MODE_OFF = 0
CAMERA_MODE_ON = 1
STATUS_NORMAL = 0
STATUS_WARN = 1

#カメラモード（ON：撮影あり、OFF：撮影なし）
camera_mode = CAMERA_MODE_ON

#各モジュール初期化
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_GPIO, GPIO.IN)
pygame.mixer.init()

#音声ファイル読み込み
pygame.mixer.music.load("./sound/bgm.mp3")
warn_voice = pygame.mixer.Sound("./sound/warning_voice.wav")
siren_sound = pygame.mixer.Sound("./sound/siren.wav")

#警告時に一定時間再検知しないための変数定義
status = STATUS_NORMAL
prev_warning_time = time.time()

#カメラ用インスタンス
mycamera = my_camera.MyCamera()

def start_motion_sensor():
    print( "監視を開始します")
    
    #起動中のBGM再生
    pygame.mixer.music.play(-1)
    
    #カメラモードの場合は画面をプレビュー
    if camera_mode == CAMERA_MODE_ON:
        mycamera.start_preview()

    global status
    while True:
        #モーションセンサー検知時
        if GPIO.input(SENSOR_GPIO) == GPIO.HIGH:
            print("侵入者発見！！")
            if status == STATUS_NORMAL:
                #警告音を出力
                siren_sound.play()
                warn_voice.play()
                
                #カメラ撮影
                if camera_mode == CAMERA_MODE_ON:
                    now = datetime.now().strftime("%Y%m%d%H%M%S")
                    path = "./" + now + ".jpg"
                    mycamera.take_picture(path)
                prev_warning_time = time.time()
                status = STATUS_WARN
        else:
            print("...")
            #前回検知から一定時間経過していたら警告音をストップし通常状態に
            if status == STATUS_WARN and (time.time() - prev_warning_time > SENSOR_WAIT_TIME):
                #警告音を停止
                siren_sound.stop()
                warn_voice.stop()
                status = STATUS_NORMAL
                
        time.sleep(SLEEP_TIME)

def stop_motion_sensor():
    print("監視を終了します")
    #BGMを停止
    pygame.mixer.music.stop()


if __name__ == "__main__":
    try:
        start_motion_sensor()
    except:
        pass
    finally:
        stop_motion_sensor()
        if camera_mode == CAMERA_MODE_ON:
            mycamera.stop_preview()
