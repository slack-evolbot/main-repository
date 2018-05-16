import RPi.GPIO as GPIO
import bme280 #大気圧・温度・湿度センサー
from tsl2561 import TSL2561 #照度センサー
import LCD_AQM0802 #LCD

import smbus  # sudo apt-get install python-smbus
import time
import csv
import datetime
import os.path

CHANNEL = 0
GAIN = 1
LED = 21

bus = smbus.SMBus(1)  # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)
GPIO.output(LED, False)
GPIO.cleanup()

if __name__ == "__main__":

    errcount = 0
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    day=datetime.datetime.now().day
    hour=datetime.datetime.now().hour

    todaydate=str(year)+"/"+str(month)+"/"+str(day)
    filename=str(year)+str(month)+str(day)+"photodata.csv"

    if not os.path.exists(filename): 
    #ファイルが存在しない場合生成。
        f = open(filename, 'w')
        f.writelines(todaydate+'\n')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["time","light","pressure","temperature","humidity"])
        f.close()

    lcd = LCD_AQM0802.i2clcd()
    lcd.clear()
    temperature, pressure, humidity = bme280.readBME280All()
    tsl = TSL2561(debug=True)
    light = tsl.lux()

    now =datetime.datetime.now()

    pressure = round(pressure,1)
    temperature = round(temperature,1)
    humidity = round(humidity,1)

    f = open(filename, 'a')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(datavalue)
    f.close()

    try:
        lcd.setaddress(0, 0)
        lcd.puts(str(hour)+":"+str(minute)+":"+str(second))
        lcd.setaddress(1, 0)
        lcd.puts(str(light).rjust(5)+"Lux")

    except IOError:
        errcount +=1
        lcd.setaddress(0, 0)
        lcd.puts(str(hour)+":"+str(minute)+":"+str(second))
        lcd.setaddress(1, 0)
        lcd.puts("IO Error")
