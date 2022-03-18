import app.config as config
import app.mqtt as mqtt

settings = config.read()
thread1 = mqtt.listener()
print('Running in background')

