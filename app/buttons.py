import app.logger as logger
import app.multithread as multithread
import app.clock as clock
import app.mqtt as mqtt
import RPi.GPIO as gpio # Import Raspberry Pi gpio library
import time

# List of buttons
buttons = ['buttonHrFw','buttonHrRv','buttonMnFw','buttonMnRv','buttonMode']

# Background process
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

# This defines gpio pins
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

# Check for button presses
def check():
    for button in buttons:
        bPin = parameters.get(button + 'Pin')
        bType = parameters.get(button + 'Type')
        # Set button type
        if bType == 'normClosed':
            if gpio.input(bPin) == gpio.LOW:
                buttonProcess(button)
        elif bType == 'normOpen':
            if gpio.input(bPin) == gpio.HIGH:
                buttonProcess(button)
        else:
            logger.log.error(f'Unknown option for bType: {{bType}}, Only accepts "normClosed" or "normOpen"')
            time.sleep(1)

# Process for when a button is pressed
def buttonProcess(button):
    # Definitions
    mode = parameters.get('mode')
    buttonModeType = parameters.get('buttonModeType')
    buttonModePin = parameters.get('buttonModePin')
    logger.log.info(mode)
    currentHr = float(parameters.get('currentHr'))
    currentMn = float(parameters.get('currentMn'))
    setHr = parameters.get('setHr')
    setMn = parameters.get('setMn')
    movementMinuteStep = parameters.get('movementMinuteStep')
    logger.log.info("Current Hour: %s Current Minute: %s" %(currentHr,currentMn))

    # When button is pressed
    logger.log.debug("Activated: %s" %(button))
    # If mode button, switch mode
    if button == 'buttonMode':
        logger.log.info("buttonMode Pressed")
        if mode == 'gameTimer':
            logger.log.info("Switching mode to Play")
            parameters['setHr'] = 12
            parameters['setMn'] = 0
            parameters['mode'] = 'play'
        elif mode == 'play':
            logger.log.info("Switching mode to gameTime")
            parameters['mode'] = 'gameTimer'
            unlock()
        else:
            logger.log.info("Unknown Mode, swtiching to gameTimer")
            parameters['mode'] == 'gameTimer'
        # Hold state if button is held
        if buttonModeType == 'normClosed':
            while gpio.input(buttonModePin) == gpio.LOW:
                time.sleep(.25)
                logger.log.debug("Button held: %s" %(button))
        elif buttonModeType == 'normOpen':
            while gpio.input(buttonModePin) == gpio.HIGH:
                time.sleep(.25)
                logger.log.debug("Button held: %s" %(button))
    else:
        # Process hour/minute
        if currentHr == setHr:
            if button == 'buttonHrFw':
                parameters['setHr'] = clock.add_subtract('hour','add',setHr,1)
            elif button == 'buttonHrRv':
                parameters['setHr'] = clock.add_subtract('hour','subtract',setHr,1)
        else:
            logger.log.info("Motor has not completed the last task, button held")
        if currentMn == setMn:
            if button == 'buttonMnFw':
                parameters['setMn'] = clock.add_subtract('minute','add',setMn,movementMinuteStep)
            elif button == 'buttonMnRv':
                parameters['setMn'] = clock.add_subtract('minute','subtract',setMn,movementMinuteStep)
        else:
            logger.log.info("Motor has not completed the last task, button held")
        logger.log.info("%s %s" %(parameters.get('setHr'),parameters.get('setMn')))
    mqtt.publish(parameters)
    time.sleep(.25)

def unlock():
    triggerHr = parameters.get('triggerHr')
    triggerMn = parameters.get('triggerMn')
    triggerPin = parameters.get('triggerPin')
    setHr = parameters.get('setHr')
    setMn = parameters.get('setMn')
    gpio.setup(triggerPin, gpio.OUT)
    
    if int(triggerHr) == int(setHr):
        logger.log.info("Hour Matched")
        if int(triggerMn) == int(setMn):
            logger.log.info("Minute Matched")
            gpio.output(triggerPin, gpio.HIGH)


