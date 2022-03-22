import app.logger as logger
import app.config as config
import app.mqtt as mqtt
import app.buttons as buttons
import time
import multiprocessing

# Prepare Global Parameters
manager = multiprocessing.Manager()
parameters = manager.dict()

# Import Global Parameters from disk
config.setup()
globalParameters = config.read()

logger.log.info('Listeners Starting')
backgroundTask1 = mqtt.listener(globalParameters)
backgroundTask2 = buttons.listener(globalParameters)

