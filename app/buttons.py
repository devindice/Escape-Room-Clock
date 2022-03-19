import app.multithread as multithread
import app.config as config
import app.clock as clock
import app.mqtt as mqtt
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

settings = config.read()
buttons = ['buttonHrFw','buttonHrRv','buttonMnFw','buttonMnRv']

@multithread.background
def listener():
    setPins()
    while True:
        check()
        time.sleep(0.01)

def setPins():
    GPIO.setwarnings(False) # Ignore warning for now
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

    for button in buttons:
        pin = settings.get(button + 'Pin')
        # Use 3v rail for buttons to pins
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

def check():
    for button in buttons:
        bPin = settings.get(button + 'Pin')
        bType = settings.get(button + 'Type')
        if bType == 'normClosed':
            if GPIO.input(bPin) == GPIO.LOW:
                print("Button %s was pushed!" %(button))
                if button == 'buttonHrFw':
                    print('adding hour')
                    clock.time('add', 'hour')
                elif button == 'buttonHrRv':
                    print('subtracting hour')
                    clock.time('subtract', 'hour')
                elif button == 'buttonMnFw':
                    print('Adding minute')
                    clock.time('add', 'minute')
                elif button == 'buttonMnRv':
                    print('Subtracting minute')
                    clock.time('subtract', 'minute')
                mqtt.publish()
                while GPIO.input(bPin) == GPIO.LOW:
                    time.sleep(0.01)
        elif bType == 'normOpen':
            if GPIO.input(bPin) == GPIO.HIGH:
                print("Button %s was pushed!" %(button))
                if button == 'buttonHrFw':
                    print('adding hour') 
                    clock.time('add', 'hour')
                elif button == 'buttonHrRv':
                    print('subtracting hour')
                    clock.time('subtract', 'hour')
                elif button == 'buttonMnFw':
                    print('Adding minute')
                    clock.time('add', 'minute')
                elif button == 'buttonMnRv':
                    print('Subtracting minute')
                    clock.time('subtract', 'minute')
                mqtt.publish()
                while GPIO.input(bPin) == GPIO.HIGH:
                    time.sleep(0.01)
        else:
            print('Unknown button type')
            time.sleep(1)


