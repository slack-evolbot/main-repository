import dht11
import RPi.GPIO as GPIO
#from time import gmtime, strftime
import time
import disp_test01
import Adafruit_BMP.BMP085 as BMP085
import lirc
 
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

#Initialize lirc
sockid = lirc.init("test05", blocking = False)

oldCodeIR="0"
dateFlg=False
flowingFlg=False

# flowing disp judge
def flowing_disp_judge(flowingFlg,line1,line2):
    if(flowingFlg):
        disp_test01.print_disp_flowing(line1,line2)
    else:
        disp_test01.print_disp(line1,line2)

try:
    while True:
        codeIR = []
        codeIR = lirc.nextcode()

        if((oldCodeIR!=codeIR and codeIR !=[]) or oldCodeIR=="1"):
            if(codeIR ==[] and oldCodeIR=="1"):
                codeIR=["1"]
                #codeIR[0]=oldCodeIR
            
            if(codeIR[0]=="next"):
                if(oldCodeIR=="9"):
                    codeIR[0]="0"
                else:
                    codeIR[0]=str(int(oldCodeIR)+1)

            if(codeIR[0]=="prev"):
                if(oldCodeIR=="0"):
                    codeIR[0]="9"
                else:
                    codeIR[0]=str(int(oldCodeIR)-1)

            if(codeIR[0]=="CH+"):
                dateFlg = True
                codeIR[0]=oldCodeIR
                
            if(codeIR[0]=="CH-"):
                dateFlg = False
                codeIR[0]=oldCodeIR

            if(codeIR[0]=="EQ"):
                flowingFlg = not flowingFlg
                codeIR[0]=oldCodeIR
                
            if(dateFlg):
                strDate = time.strftime("%Y.%m.%d(%a)", time.gmtime())
            else:
                strDate = ""

            if(codeIR[0]!="prev" or codeIR[0]!="next" or codeIR[0]!="CH+" or codeIR[0]!="CH-" or codeIR[0]!="EQ"):
                oldCodeIR=codeIR[0]

            result = instance.read()
            if result.is_valid():
                print("temp:"+str(result.temperature)+" C") #「lcd_string」を「print」に置き換えて、第2引数を削除した
                print("humid:"+str(result.humidity)+"%") #「lcd_string」を「print」に置き換えて、第2引数を削除した
                print("pressure:"+str(sensor.read_pressure())+" Pa")
            
                print("buttonID:"+codeIR[0])

                if(codeIR[0]=="0"):
                    #disp_test01.print_disp(str(result.temperature)+"C",str(result.humidity)+"%",str(sensor.read_pressure())+"Pa")
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0]),"")

                elif(codeIR[0]=="1"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0]),"LCHIKA TEST")
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
                            
                elif(codeIR[0]=="2"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,"")

                elif(codeIR[0]=="3"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.temperature)+"C")

                elif(codeIR[0]=="4"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.humidity)+"%")

                elif(codeIR[0]=="5"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(sensor.read_pressure())+"Pa")

                elif(codeIR[0]=="6"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.temperature)+"C "+str(result.humidity)+"%")

                elif(codeIR[0]=="7"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.temperature)+"C "+str(sensor.read_pressure())+"Pa")

                elif(codeIR[0]=="8"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.humidity)+"% "+str(sensor.read_pressure())+"Pa")

                elif(codeIR[0]=="9"):
                    flowing_disp_judge(flowingFlg,"CH"+str(codeIR[0])+" "+strDate,str(result.temperature)+"C "+str(result.humidity)+"% "+str(sensor.read_pressure())+"Pa")
                
except KeyboardInterrupt:
    pass

finally:
    disp_test01.finally_disp()

GPIO.cleanup()
