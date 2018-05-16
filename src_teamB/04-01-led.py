import RPi.GPIO as GPIO
from time import sleep

import wiringpi

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

try:
    while True:
        if (wiringpi.digitalRead(button_pin) == 0):
            GPIO.output(25, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(25, GPIO.LOW)
            sleep(0.5)
        else:
            #no action

except KeyboardInterrupt:
    pass

GPIO.cleanup()

