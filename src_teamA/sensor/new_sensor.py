# -*- coding: utf-8 -*- 
import RPi.GPIO as GPIO
import time
import datetime
import pygame.mixer
import requests
import json

#define
SLEEP_TIME = 1
SENSOR_GPIO = 5
SENSOR_WAIT_TIME = 3
warningFlg = False
stopEvent = False

#init
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_GPIO, GPIO.IN)
pygame.mixer.init()

#LINE
LINE_POST_URL = "https://api.line.me/v2/bot/message/push"
LINE_POST_ID = "Uacfc50da8bb896a9be0035f75531dac1"
LINE_POST_TYPE_TEXT = "text"
LINE_POST_TYPE_STAMP = "sticker"
ACCESS_TOKEN = "bMSdJhXAhnNZssru/uBNuWYP/19STcZ7+Vb/XJd+DnpWNu5csAqyEF4pOdh8XHVgdYf6cC6wCmm2pLRTqWJj6Uf5jmf6eZgjH8BsoQUq6HJR4vx4uBws8qWn7GwXaSjWTxzkXZy/zKY2fmYisZ6RLgdB04t89/1O/w1cDnyilFU="
headers = {
    "Content-Type" : "application/json", 
    "Authorization" : "Bearer "+ ACCESS_TOKEN
}

#load sound
pygame.mixer.music.load("./sound/bgm.mp3")
warningVoice = pygame.mixer.Sound("./sound/warning_voice.wav")
sirenSound = pygame.mixer.Sound("./sound/siren.wav")

beforeWarningtime = time.time()

class MothionSensor():

    def startMotionSensor(self):
        print( "START!")
        
        #LINE Message
        textData = { 
            "to": LINE_POST_ID, 
            "messages": [ 
                { 
                    "type": LINE_POST_TYPE_TEXT, 
                    "text": "監視を開始しました"
                } 
            ] 
        } 
        requests.post(LINE_POST_URL ,data=json.dumps(textData), headers = headers)
        
        #LINE Stamp
        stampData = { 
            "to": LINE_POST_ID, 
            "messages": [ 
                { 
                    "type": LINE_POST_TYPE_STAMP, 
                    "stickerId": "138",
                    "packageId": "1"
                } 
            ] 
        } 
        requests.post(LINE_POST_URL ,data=json.dumps(stampData), headers = headers)
        
        #BGM play
        pygame.mixer.music.play(-1)


        #sensor start
        global warningFlg
        while not self.stopEvent.is_set():
            if GPIO.input(SENSOR_GPIO) == GPIO.HIGH:
                print( "WARNING!!")
                if warningFlg == False:
                    
                    #sound play
                    sirenSound.play()
                    warningVoice.play()
                    
                    #LINE Message
                    textData = { 
                        "to": LINE_POST_ID, 
                        "messages": [ 
                            { 
                                "type": LINE_POST_TYPE_TEXT, 
                                "text": "侵入者を検知しました"
                            } 
                        ] 
                    }
                    requests.post(LINE_POST_URL ,data=json.dumps(textData), headers = headers)
        
                    #LINE Stamp
                    stampData = { 
                        "to": LINE_POST_ID, 
                        "messages": [ 
                            { 
                                "type": LINE_POST_TYPE_STAMP, 
                                "stickerId": "6",
                                "packageId": "1"
                            } 
                        ] 
                    } 
                    requests.post(LINE_POST_URL ,data=json.dumps(stampData), headers = headers)
                    
                    beforeWarningtime = time.time()
                    warningFlg = True
            else:
                print("...")
                if (warningFlg == True) and (time.time() - beforeWarningtime > SENSOR_WAIT_TIME):
                    #sound stop
                    sirenSound.stop()
                    warningVoice.stop()
                    warningFlg = False
                    
            time.sleep(SLEEP_TIME)

    def stopMotionSensor(self):
        print( "STOP!")
        
        #LINE Message
        textData = { 
            "to": LINE_POST_ID, 
            "messages": [ 
                { 
                    "type": LINE_POST_TYPE_TEXT, 
                    "text": "監視を終了しました"
                } 
            ] 
        } 
        requests.post(LINE_POST_URL ,data=json.dumps(textData), headers = headers)
        
        #LINE Stamp
        stampData = { 
            "to": LINE_POST_ID, 
            "messages": [ 
                { 
                    "type": LINE_POST_TYPE_STAMP, 
                    "stickerId": "408",
                    "packageId": "1"
                } 
            ] 
        } 
        requests.post(LINE_POST_URL ,data=json.dumps(stampData), headers = headers)

        #BGM stop
        pygame.mixer.music.stop()
        
        #sensor stop
        self.stopEvent.set()
        self.thread.join()
