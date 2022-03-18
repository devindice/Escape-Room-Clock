import app.multithread as multithread
import paho.mqtt.client as mqtt
import json

@multithread.background
def listener():
    print('MQTT Listener Started')
    subclient = mqtt.Client("DynamicDetectorSub")
    subclient.on_message = on_message
    subclient.connect('192.168.185.2')
    subclient.subscribe("/pi/clock/data", 2)
    subclient.loop_forever()

def on_message(client, userdata, msg):
    message = msg.payload
    message = json.loads(message.decode('utf8'))
    for key in ['triggerHour', 'triggerMinute','reset','unlock','autoResetSeconds']:
        if key in message.keys():
            value = message.get(key) 
            print("MQTT - Set %s: %s" %(key,value))
