import app.logger as logger
import app.multithread as multithread
import app.config as config
import paho.mqtt.client as mqtt
import json

settings = config.read()
mqttClient = 'RPi_Clock'
mqttBroker = settings.get('mqttBrokerAddress')
mqttTopicOut = settings.get('mqttTopicOut')
mqttTopicIn = settings.get('mqttTopicIn')

@multithread.background
def listener():

    settings = config.read()
    if settings.get('mqttEnable') == "true":
        try:
            subclient = mqtt.Client(mqttClient + 'In')
            subclient.on_message = on_message
            subclient.connect('%s' %(mqttBroker))
            subclient.subscribe('%s' %(mqttTopicIn), 2)
            logger.log.info("MQTT - Subscribed to %s on %s" %(mqttTopicIn,mqttBroker))
            subclient.loop_forever()
        except:
            logger.log.info("MQTT - Unable to subscribe to %s on %s" %(mqttTopic,mqttBroker))
    else:
        logger.log.info('MQTT - Subscription Disabled')

def on_message(client, userdata, msg):
    settings = config.read()
    message = msg.payload
    message = json.loads(message.decode('utf8'))
    for key in settings.keys():
        if key in message.keys():
            value = message.get(key) 
            settings[key] = value
            logger.log.info("MQTT - Set %s: %s" %(key,value))
    config.write(settings)

def publish():
    settings = config.read()
    if settings.get('mqttEnable') == "true":
        try:
            logger.log.info("MQTT - Publish")
            client = mqtt.Client(mqttClient + 'Out')
            client.connect(mqttBroker)
            client.publish(mqttTopicOut,json.dumps(settings))
        except:
            logger.log.info("Unable to publish mqtt messsage")
