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
    try:
        logger.log.debug("Reading config")
        settings = config.read()
        if settings.get('mqttEnable') == "true":
            try:
                subclient = mqtt.Client(mqttClient + 'In')
                subclient.on_message = on_message
                subclient.connect('%s' %(mqttBroker))
                subclient.subscribe('%s' %(mqttTopicIn), 2)
                logger.log.info("Subscribed to %s on %s" %(mqttTopicIn,mqttBroker))
                try:
                    subclient.loop_forever()
                except:
                    logger.log.error("mqtt client closed", exc_info=True)
            except:
                logger.log.error("Unable to subscribe to %s on %s" %(mqttTopic,mqttBroker), exc_info=True)
        else:
            logger.log.info('Subscription Disabled')
    except:
        logger.log.critical("Listener Crashed", exc_info=True)

def on_message(client, userdata, msg):
    logger.log.debug("Reading changes from other processes")
    settings = config.read()
    message = msg.payload
    message = json.loads(message.decode('utf8'))
    logger.log.debug("Message Received - \"%s\"" %(message))
    for key in message:
        value = message.get(key)
        if key in settings.keys():
            logger.log.info("Setting %s to %s" %(key,value))
            settings[key] = value
            config.write(settings)
        else:
            logger.log.warning("Received key %s is not valid " %(key))

    #for key in settings.keys():
    #    if key in message.keys():
    #        value = message.get(key) 
    #        settings[key] = value
    #        logger.log.info("Set %s: %s" %(key,value))
    #    elif key not in message.keys():
    #        value = message.get(key)
    #        logger.log.error(f"Unknown key: %s; Value: %s" %(key,value))
    #config.write(settings)

def publish():
    logger.log.debug("Reading changes from other processes")
    settings = config.read()
    if settings.get('mqttEnable') == "true":
        try:
            logger.log.debug("Sending Message")
            client = mqtt.Client(mqttClient + 'Out')
            client.connect(mqttBroker)
            client.publish(mqttTopicOut,json.dumps(settings))
        except:
            logger.log.error("Messsage Failed to Send", exc_info=True)
