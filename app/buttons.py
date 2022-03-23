import app.logger as logger
import app.multithread as multithread
import app.clock as clock
import app.mqtt as mqtt
import RPi.GPIO as gpio # Import Raspberry Pi gpio library
import time


buttons = ['buttonHrFw','buttonHrRv','buttonMnFw','buttonMnRv']

@multithread.background
def listener(globalParameters):
    global parameters
    parameters = globalParameters
    try:
        setPins()
        while True:
            check()
            time.sleep(0.01)
    except:
        logger.log.critical("Listener Crashed", exc_info=True)

def setPins():
    logger.log.debug("Setting board and button pins for input")
    try:
        gpio.setwarnings(False) # Ignore warning for now
        gpio.setmode(gpio.BCM) # Use physical pin numbering
    except:
        logger.log.error("An error occured while configuring board", exc_info=True)
    try:
        for button in buttons:
            pin = parameters.get(button + 'Pin')
            # Use 3v rail for buttons to pins
            gpio.setup(pin, gpio.IN, pull_up_down=gpio.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    except:
        logger.log.error("An error occured while configuring pins", exc_info=True)

def check():
    for button in buttons:
        bPin = parameters.get(button + 'Pin')
        bType = parameters.get(button + 'Type')
        if bType == 'normClosed':
            if gpio.input(bPin) == gpio.LOW:
                buttonProcess(button)
        elif bType == 'normOpen':
            if gpio.input(bPin) == gpio.HIGH:
                buttonProcess(button)
        else:
            logger.log.error(f'Unknown option for bType: {{bType}}, Only accepts "normClosed" or "normOpen"')
            time.sleep(1)

def buttonProcess(button):
    logger.log.debug("Activated: %s" %(button))
    if button == 'buttonHrFw':
        clock.time(parameters,'add', 'hour')
    elif button == 'buttonHrRv':
        clock.time(parameters,'subtract', 'hour')
    elif button == 'buttonMnFw':
        clock.time(parameters,'add', 'minute')
    elif button == 'buttonMnRv':
        clock.time(parameters,'subtract', 'minute')
    mqtt.publish(parameters)
