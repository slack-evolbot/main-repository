import time
import disp_test01
import re

try:
    strTest="123456789012345678901234567890"
    rex = ', |\'|\[|\]'
    sprStr = list(strTest)

    for num in range(0,len(strTest)-1):
        relpaceStr = str(sprStr[num:len(strTest)])

        print re.sub(rex,'',relpaceStr)
            
        disp_test01.print_disp(re.sub(rex,'',relpaceStr),"")
        time.sleep(0.5)

        if(len(re.sub(rex,'',relpaceStr))-17<0):
            break

except KeyboardInterrupt:
    pass

