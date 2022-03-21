import app.logger as logger
import app.mqtt as mqtt
import app.buttons as buttons

logger.log.info('Listeners Starting')
backgroundTask1 = mqtt.listener()
backgroundTask2 = buttons.listener()
