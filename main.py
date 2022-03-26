import app.logger as logger
import app.config as config
import app.mqtt as mqtt
import app.buttons as buttons
import app.motor as motor
import app.control as control
import time
import multiprocessing
import RPi.GPIO as gpio 


# Import parameters from disk
parameters = config.parameters

triggerPin = parameters.get('triggerPin')
gpio.setup(triggerPin, gpio.OUT)
gpio.output(triggerPin, gpio.LOW)

logger.log.info('Services Starting')
Service1 = mqtt.service(parameters)
Service2 = buttons.service(parameters)
Service3 = config.service(parameters)
Service4 = motor.service(parameters)
Service5 = control.service(parameters)

