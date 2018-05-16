import lirc
import time
import subprocess


#Initialize lirc
sockid = lirc.init("test05", blocking = False)

try:
    while True:
        codeIR = lirc.nextcode()

        print(codeIR !=[])
        
        if(codeIR !=[]):
            #codeIR = lirc.nextcode()
            print("BUTTON_ID:"+codeIR[0])

        else: 
            time.sleep(3)

except KeyboardInterrupt:
    pass

