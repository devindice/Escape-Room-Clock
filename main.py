import app.config as config
import app.mqtt as mqtt
import app.buttons as buttons
import time

settings = config.read()
backgroundTask1 = mqtt.listener()
backgroundTask2 = buttons.listener()

#buttons.setPins()
#while True:
#    buttons.check()
#    time.sleep(0.01)
