import app.logger as logger
import app.config as config
import app.mqtt as mqtt
import app.buttons as buttons
import time
import multiprocessing

# Import parameters from disk
parameters = config.parameters

logger.log.info('Listeners Starting')
backgroundTask1 = mqtt.listener(parameters)
backgroundTask2 = buttons.listener(parameters)
backgroundTask3 = config.listener(parameters)

