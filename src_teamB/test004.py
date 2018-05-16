import os
import sys
import time

try:
        while True:
            
            os.system('bto_advanced_USBIR_cmd -r')
            time.sleep(3)
            print("test1 "+str(os.system('bto_advanced_USBIR_cmd -g')))
            os.system('bto_advanced_USBIR_cmd -s')
            print("test2 "+str(os.system('bto_advanced_USBIR_cmd -g')))

except KeyboardInterrupt:
        pass
