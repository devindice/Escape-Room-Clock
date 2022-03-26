import app.logger as logger
import app.multithread as multithread
import paho.mqtt.client as mqtt
import json

@multithread.background
def service(globalParameters):
    global parameters
    parameters = globalParameters
    mqttClient = 'RPi_Clock'
    mqttBroker = parameters.get('mqttBrokerAddress')
    mqttTopicOut = parameters.get('mqttTopicOut')
    mqttTopicIn = parameters.get('mqttTopicIn')
    try:
        if parameters.get('mqttEnable') == "true":
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
    message = msg.payload
    message = json.loads(message.decode('utf8'))
    logger.log.info("Message Received - \"%s\"" %(message))
    for key in message:
        value = message.get(key)
        if key in parameters.keys():
            if key == 'defaultHr':
                value = float(value) / 5
            elif key == 'defaultMn':
                value = float(value)
            logger.log.debug("Setting %s to %s" %(key,value))
            parameters[key] = value
        else:
            logger.log.warning("Received key %s is not valid " %(key))

def publish(parameters):
    mqttClient = 'RPi_Clock'
    mqttBroker = parameters.get('mqttBrokerAddress')
    mqttTopicOut = parameters.get('mqttTopicOut')
    mqttTopicIn = parameters.get('mqttTopicIn')
    if parameters.get('mqttEnable') == "true":
        try:
            logger.log.debug("Sending MQTT Message")
            client = mqtt.Client(mqttClient + 'Out')
            client.connect(mqttBroker)
            client.publish(mqttTopicOut,json.dumps(parameters))
        except:
            logger.log.error("Messsage Failed to Send", exc_info=True)
