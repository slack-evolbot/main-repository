import dht11
import RPi.GPIO as GPIO
import time
 
# Define GPIO to LCD mapping
Temp_sensor=4
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
GPIO.cleanup()

instance = dht11.DHT11(pin = Temp_sensor)

try:
    while True:
        #get DHT11 sensor value
        result = instance.read()
        if result.is_valid():
            print("temp:"+str(result.temperature)+" C") #「lcd_string」を「print」に置き換えて、第2引数を削除した
            # print("humid:"+str(result.humidity)+"%") 「lcd_string」を「print」に置き換えて、第2引数を削除した

            if(result.temperature >= 30):
                print("over 30C")
                time.sleep(3) # 3 second delay
                
            else:
                print("no action")
                time.sleep(3) # 3 second delay

except KeyboardInterrupt:
    pass

GPIO.cleanup()
