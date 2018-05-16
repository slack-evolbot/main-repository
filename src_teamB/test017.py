import subprocess
try:
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi "吉村が可愛いですね笑" | aplay', shell=True)
except:
    print("Error.")
