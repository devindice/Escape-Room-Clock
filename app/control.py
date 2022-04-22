import app.logger as logger
import app.multithread as multithread
import app.mqtt as mqtt
import time
import RPi.GPIO as gpio

# Background process
@multithread.background
def service(globalParameters):
    global parameters
    parameters = globalParameters
    try:
        while True:
            check()
            time.sleep(0.1)
    except:
        logger.log.critical("Listener Crashed", exc_info=True)

def check():
    addNewParams()
    reset = parameters.get('reset')
    unlock = parameters.get('unlock')
    unlockLastState = parameters.get('unlockLastState')
    defaultHr = float(parameters.get('defaultHr'))
    currentHr = float(parameters.get('currentHr'))
    triggerPin = parameters.get('triggerPin')
    if reset == 'true':
        logger.log.info('Resetting')
        parameters['reset'] = 'false'
        parameters['unlock'] = 'false'
        parameters['unlockLastState'] = 'false'
        parameters['setHr'] = 12
        parameters['setMn'] = 0
        parameters['mode'] = 'gameTimer'
        gpio.output(triggerPin, gpio.HIGH)
        mqtt.publish(parameters)
    if unlock == 'true' and unlockLastState == 'false':
        gpio.output(triggerPin, gpio.LOW)
        time.sleep(0.5)
        gpio.output(triggerPin, gpio.HIGH)
        parameters['unlockLastState'] = 'true'
        mqtt.publish(parameters)
        parameters['unlock'] = 'true'
        logger.log.info('Relay Triggered')
    if defaultHr < 1:
        parameters['defaultHr'] = defaultHr + 12
        logger.log.debug('Fixing Invalid defaultHr')
    if currentHr < 1:
        parameters['currentHr'] = currentHr + 12
        logger.log.debug('Fixing Invalid currentHr')


def addNewParams():
    if ! parameters.get('unlockLastState'):
        parameters['unlockLastState'] = parameters.get('unlock')
