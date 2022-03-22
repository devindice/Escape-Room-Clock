import app.logger as logger
import pathlib
import json
from os.path import exists

configFile = 'config.json'
appPath = str(pathlib.Path(__file__).parent.resolve()).removesuffix('app')

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
        'resetHr':12,
        'resetMn':0,
        'limitRotationHr':'?',
        'limitRotationMn':'?',
        'triggerHr':1,
        'triggerMn':0,
        'triggerPin':37,
        'triggerDelay':3,
        'triggerDuration':'?',
        'movementDelay':0.25,
        'movemnentRotation':'full',
        'movementMinuteStep':'1',
        'motorHr':'motor1',
        'motorMn':'motor2',
        'motorReverse1':'false',
        'motorReverse2':'true',
        'mqttEnable':'false',
        'mqttBrokerAddress':'192.168.1.100',
        'mqttTopicIn':'/pi/clock/in',
        'mqttTopicOut':'/pi/clock/out',
        'autoResetSeconds':300,
        'timeoutMinutes':20,
        'reduceDrift':'true?',
        'calibrateHr':'',
        'calibrateMn':'',
        'autoUpdate':'true',
        'buttonHrFwPin':12,
        'buttonHrRvPin':16,
        'buttonMnFwPin':20,
        'buttonMnRvPin':21,
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
        settings = json.loads(data)
    except:
        logger.log.warning('Unable to open the config, another process may also be writing', exc_info=True)
        time.sleep(0.05)
        data = False
        while data:
            with open(f'{appPath}{configFile}') as f:
                data = f.read()
        settings = json.loads(data)
    return settings

def write(settings):
    try:
        logger.log.debug("Writing changes")
        f = open(f'{appPath}{configFile}',"w")
        json.dump(settings,f)
        f.close()
    except:
        logger.log.error('Unable to write config')

x = 0

