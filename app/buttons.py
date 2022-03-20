import app.logger as logger
import app.multithread as multithread
import app.config as config
import app.clock as clock
import app.mqtt as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

buttons = ['buttonHrFw','buttonHrRv','buttonMnFw','buttonMnRv']

@multithread.background
def listener():
    try:
        logger.log.debug("Reading config")
        global settings
        settings = config.read()
        setPins()
        while True:
            check()
            time.sleep(0.01)
    except:
        logger.log.critical("Listener Crashed", exc_info=True)

def setPins():
    logger.log.debug("Setting board and button pins for input")
    try:
        GPIO.setwarnings(False) # Ignore warning for now
        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    except:
        logger.log.error("An error occured while configuring board", exc_info=True)
    try:
        for button in buttons:
            pin = settings.get(button + 'Pin')
            # Use 3v rail for buttons to pins
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    except:
        logger.log.error("An error occured while configuring pins", exc_info=True)

def check():
    for button in buttons:
        bPin = settings.get(button + 'Pin')
        bType = settings.get(button + 'Type')
        if bType == 'normClosed':
            if GPIO.input(bPin) == GPIO.LOW:
                logger.log.debug("Activated: %s" %(button))
                if button == 'buttonHrFw':
                    clock.time('add', 'hour')
                elif button == 'buttonHrRv':
                    clock.time('subtract', 'hour')
                elif button == 'buttonMnFw':
                    clock.time('add', 'minute')
                elif button == 'buttonMnRv':
                    clock.time('subtract', 'minute')
                mqtt.publish()
                while GPIO.input(bPin) == GPIO.LOW:
                    logger.log.debug("Held: %s" %(button))
                    time.sleep(0.1)
        elif bType == 'normOpen':
            if GPIO.input(bPin) == GPIO.HIGH:
                logger.log.debug("Activated: %s" %(button))
                if button == 'buttonHrFw':
                    clock.time('add', 'hour')
                elif button == 'buttonHrRv':
                    clock.time('subtract', 'hour')
                elif button == 'buttonMnFw':
                    clock.time('add', 'minute')
                elif button == 'buttonMnRv':
                    clock.time('subtract', 'minute')
                mqtt.publish()
                while GPIO.input(bPin) == GPIO.HIGH:
                    logger.log.debug("Held: %s" %(button))
                    time.sleep(0.1)
        else:
            logger.log.error(f'Unknown option for bType: {{bType}}, Only accepts "normClosed" or "normOpen"')
            time.sleep(1)

