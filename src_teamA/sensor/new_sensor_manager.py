# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import threading
import new_sensor
import threading

#MQTT define
TOKEN = "token_pEuhRkO1Nnb6Zb6k"
HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
TOPIC = "pichannel/action"
CACERT = "/home/pi/sensor/mqtt/mqtt.beebotte.com.pem"

#sensor class init
motionSensor = new_sensor.MothionSensor()
sensorRunningFlg = False

#MQTT subscribe
def on_connect(client, userdata, flags, respons_code):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global sensorRunningFlg
    if sensorRunningFlg == False:
        motionSensor.stopEvent = threading.Event()
        motionSensor.thread = threading.Thread(target=motionSensor.startMotionSensor)
        motionSensor.thread.start()
        sensorRunningFlg = True
    else:
        motionSensor.stopMotionSensor()
        sensorRunningFlg = False

client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CACERT)
client.connect(HOSTNAME, port=PORT, keepalive=60)
client.loop_forever()
