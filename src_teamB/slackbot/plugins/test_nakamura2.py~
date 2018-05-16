import dht11
import RPi.GPIO as GPIO
import time
import disp_test01
import Adafruit_BMP.BMP085 as BMP085
 
# Define GPIO to LCD mapping
Temp_sensor=4

# Define LED Out temperature Pin Number
Led_out_temperature=17

# Define LED In Pin Number
#Led_in=??

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

GPIO.setup(Led_out_temperature, GPIO.OUT)
#GPIO.setup(Led_in, GPIO.IN)

instance = dht11.DHT11(pin = Temp_sensor)

sensor = BMP085.BMP085()

try:
    while True:
        #get DHT11 sensor value
        result = instance.read()
        if result.is_valid():
            print("temp:"+str(result.temperature)+" C") #「lcd_string」を「print」に置き換えて、第2引数を削除した
            print("humid:"+str(result.humidity)+"%") #「lcd_string」を「print」に置き換えて、第2引数を削除した
            #print('Pressure:{0:0.2f} Pa'.format(sensor.read_pressure()))
            print("pressure:"+str(sensor.read_pressure())+" Pa")
            disp_test01.print_disp("",str(result.temperature)+"C"+" "+str(result.humidity)+"%"+" "+str(sensor.read_pressure())+"Pa")

            if(result.temperature >= 29):
                print("over 29C")

                start_time = time.clock()
                end_time = time.clock()
                while(float(end_time)-float(start_time)<=0.009):
                    GPIO.output(Led_out_temperature, GPIO.HIGH)
                    time.sleep(0.1)
                    GPIO.output(Led_out_temperature, GPIO.LOW)
                    time.sleep(0.1)
                    end_time = time.clock()

            elif(result.temperature >= 27):
                print("over 27C")

                start_time = time.clock()
                end_time = time.clock()
                while(float(end_time)-float(start_time)<=0.009):
                    GPIO.output(Led_out_temperature, GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(Led_out_temperature, GPIO.LOW)
                    time.sleep(1)
                    end_time = time.clock()
                
            else:
                print("no action")
                GPIO.output(Led_out_temperature, GPIO.LOW)
                time.sleep(3)

except KeyboardInterrupt:
    pass

finally:
    disp_test01.finally_disp()

GPIO.cleanup()
