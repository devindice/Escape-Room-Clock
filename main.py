import app.logger as logger
import app.config as config
import app.mqtt as mqtt
import app.buttons as buttons
import app.motor as motor
import time
import multiprocessing
import RPi.GPIO as gpio 


# Import parameters from disk
parameters = config.parameters

triggerPin = parameters.get('triggerPin')
gpio.setup(triggerPin, gpio.OUT)
gpio.output(triggerPin, gpio.LOW)

logger.log.info('Listeners Starting')
backgroundTask1 = mqtt.listener(parameters)
backgroundTask2 = buttons.listener(parameters)
backgroundTask3 = config.listener(parameters)
backgroundTask4 = motor.listener(parameters)

