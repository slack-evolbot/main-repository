import disp_test01
from time import sleep
import subprocess

#disp_test01.print_disp("1", "2")
#sleep(10)

#response = subprocess.check_output("traceroute 8.8.8.8", universal_newlines=True, shell=True)

#counter = 1
#for resp in str(response).split("\n"):
#    print(str(counter) + ":" + resp)
#    counter += 1
    


response1 = subprocess.call("ping -c 1 28.18.28.18", shell=True)
#response1 = subprocess.check_call("ls")

print(response1)
