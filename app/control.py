import app.logger as logger
import app.multithread as multithread
import time
import RPi.GPIO as gpio
import app.mqtt as mqtt

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
    reset = parameters.get('reset')
    unlock = parameters.get('unlock')
    defaultHr = float(parameters.get('defaultHr'))
    currentHr = float(parameters.get('currentHr'))
    triggerPin = parameters.get('triggerPin')
    if reset == 'true':
        logger.log.info('Resetting')
        parameters['reset'] = 'false'
        parameters['unlock'] = 'false'
        parameters['setHr'] = 12
        parameters['setMn'] = 0
        parameters['mode'] = 'gameTimer'
        gpio.output(triggerPin, gpio.LOW)
        mqtt.publish(parameters)
    if unlock == 'true':
        gpio.output(triggerPin, gpio.HIGH)
        mqtt.publish(parameters)
        parameters['unlock'] = 'True'
        logger.log.info('Relay Triggered')
    if defaultHr < 1:
        parameters['defaultHr'] = defaultHr + 12
        logger.log.debug('Fixing Invalid defaultHr')
    if currentHr < 1:
        parameters['currentHr'] = currentHr + 12
        logger.log.debug('Fixing Invalid currentHr')
