import RPi.GPIO as GPIO

print("hello world")
#はじめて書いたコード


print(4649)
print("4"+"6"+"4"+"9")
#出力結果が同じになるはず・・・


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

GPIO.setup(17, GPIO.OUT)

GPIO.output(17, GPIO.HIGH)
GPIO.output(17, GPIO.LOW)
