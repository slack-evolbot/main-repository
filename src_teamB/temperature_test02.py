import dht11
import RPi.GPIO as GPIO
import time
 
# Define GPIO to LCD mapping
Temp_sensor=4

# Define LED Out Pin Number
Led_out=17

# Define LED In Pin Number
#Led_in=??
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

GPIO.setup(Led_out, GPIO.OUT)
#GPIO.setup(Led_in, GPIO.IN)

instance = dht11.DHT11(pin = Temp_sensor)

try:
    while True:
        #get DHT11 sensor value
        result = instance.read()
        if result.is_valid():
            print("temp:"+str(result.temperature)+" C") #「lcd_string」を「print」に置き換えて、第2引数を削除した
            # print("humid:"+str(result.humidity)+"%") 「lcd_string」を「print」に置き換えて、第2引数を削除した

            if(result.temperature >= 31):
                print("over 31C")

                start_time = time.clock()
                end_time = time.clock()
                while(float(end_time)-float(start_time)<=0.009):
                    GPIO.output(Led_out, GPIO.HIGH)
                    time.sleep(0.1)
                    GPIO.output(Led_out, GPIO.LOW)
                    time.sleep(0.1)
                    end_time = time.clock()

            elif(result.temperature >= 29):
                print("over 29C")

                start_time = time.clock()
                end_time = time.clock()
                while(float(end_time)-float(start_time)<=0.009):
                    GPIO.output(Led_out, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(Led_out, GPIO.LOW)
                    time.sleep(1)
                    end_time = time.clock()
                
            else:
                print("no action")
                GPIO.output(Led_out, GPIO.LOW)
                time.sleep(3)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
