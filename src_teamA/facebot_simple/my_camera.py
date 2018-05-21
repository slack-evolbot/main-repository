# -*- coding: utf-8 -*-
import time
import picamera

camera = picamera.PiCamera()

class MyCamera():
    #初期化    
    def __init__(self):
        camera.resolution = (768, 768) #写真サイズ
        camera.vflip = True #映像を上下逆に
        camera.hflip = True #映像を左右逆に
        camera.brightness = 60 #明るさを60に
        camera.annotate_foreground = picamera.Color("white")
        camera.annotate_background = picamera.Color("black")
    
    #1枚撮影
    def take_picture(self, path):
        #写真撮影
        camera.capture(path) #撮影

    #指定回数撮影
    def take_pictures(self, path, count):
        print(str(count) + "回連続で撮影します。\n顔の角度をゆっくり変え続けてください。")
        time.sleep(3)
        camera.start_preview(fullscreen=False, window=(100,100,256,192)) #プレビューの表示
        #写真撮影
        for i in range(count): #引数のcount回分撮影
            print(i+1)
            camera.capture(path + str(i) + ".jpg")
        camera.stop_preview()
        
    def start_preview(self):
        camera.start_preview(fullscreen=False, window=(50,50,768,768))
        time.sleep(3) #このスリープがないとカクカクしてしまう
            
    def display_text(self, text):
        camera.annotate_text = text

    def stop_preview(self):
        camera.stop_preview()
