import app.logger as logger
import app.multithread as multithread
from os.path import exists
import pathlib
import json
import time

configFile = 'config.json'
appPath = str(pathlib.Path(__file__).parent.resolve()).removesuffix('app')

@multithread.background
def service(parameters):
    oldParameters = str(parameters)
    try:
        while True:
            if oldParameters != str(parameters):
                logger.log.debug('Writing changes to disk')
                write(parameters)
                oldParameters = str(parameters)
            time.sleep(1)
    except:
        logger.log.critical('Listener crashed', exc_info=True)

def setup():
    if exists(f'{appPath}{configFile}'):
        logger.log.debug("Config file exists")
    else:
        logger.log.warning("Config does not exist, creating default config")
        settings = {
        'ticksFullRotation':12000,
        'style':'interleave',
        'currentHr':12,
        'currentMn':0,
        'defaultHr':12,
        'defaultMn':0,
        'defaultTimer':'true',
        'setHr':12,
        'setMn':0,
        'mode':'gameTimer',
        'triggerHr':1,
        'triggerMn':0,
        'triggerPin':26,
        'movementDelay':0.25,
        'movementMinuteStep':'1',
        'motorHr':'motor1',
        'motorMn':'motor2',
        'motor1Reverse':'false',
        'motor2Reverse':'false',
        'mqttEnable':'false',
        'mqttBrokerAddress':'192.168.1.100',
        'mqttTopicIn':'/pi/clock/in',
        'mqttTopicOut':'/pi/clock/out',
        'autoUpdate':'true',
        'buttonModePin':19,
        'buttonHrFwPin':12,
        'buttonHrRvPin':16,
        'buttonMnFwPin':20,
        'buttonMnRvPin':21,
        'buttonModeType':'normOpen',
        'buttonHrFwType':'normOpen',
        'buttonHrRvType':'normOpen',
        'buttonMnFwType':'normOpen',
        'buttonMnRvType':'normOpen',
        'reset':'false',
        'unlock':'false'
        }
        write(settings)    

def read():
    try:
        with open(f'{appPath}{configFile}') as f:
            data = f.read()
        parameters = json.loads(data)
    except:
        logger.log.warning('Unable to open the config, another process may also be writing', exc_info=True)
        time.sleep(0.05)
        data = False
        while data:
            with open(f'{appPath}{configFile}') as f:
                data = f.read()
        settings = json.loads(data)
    return parameters

def write(parameters):
    try:
        f = open(f'{appPath}{configFile}',"w")
        json.dump(parameters,f)
        f.close()
    except:
        logger.log.error('Unable to write config')
setup()

parameters = read()
