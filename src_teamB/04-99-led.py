import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

#switch = GPIO.LOW

try:
    while True:
        if  GPIO.input(24) == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(25, GPIO.LOW)
            sleep(0.5)
        else:
            sleep(1)

except KeyboardInterrupt:
    pass

GPIO.cleanup()

