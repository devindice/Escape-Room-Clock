import pathlib
import json

configFile = 'config.json'
appPath = str(pathlib.Path(__file__).parent.resolve()).removesuffix('app')

def read():
    try:
        with open(f'{appPath}{configFile}') as f:
            data = f.read()
        settings = json.loads(data)
    except:
        print("Config does not exist, creating default config")
        settings = {'ticksFullRotation':0,'style':'interleave','currentHr':12,'currentMn':0,'resetHr':12,'resetMn':0,'limitRotationHr':0,'limitRotationMn':0,'triggerHr':1,'triggerMn':0,'triggerPin':37,'triggerDelay':3,'triggerDuration':0.25,'movementDelay':0.25,'movemnentRotation':'full','movementMinuteStep':'5','motor1':'hour','motor2':'minute','movementSnap':'true','mqttEnable':'false','mqttBrokerAddress':'192.168.1.100','mqttTopicIn':'/pi/clock/in','mqttTopicOut':'/pi/clock/out','autoResetSeconds':300,'reduceDrift':'true','mode':'run','calibrateMethod':4,'autoUpdate':'true','buttonHrFwPin':32,'buttonHrRvPin':36,'buttonMnFwPin':38,'buttonMnRvPin':40,'buttonHrFwType':'normOpen','buttonHrRvType':'normOpen','buttonMnFwType':'normOpen','buttonMnRvType':'normOpen','reset':'false','unlock':'false'}
        write(settings)    
    return settings

def write(settings):
    try:
        f = open(f'{appPath}{configFile}',"w")
        json.dump(settings,f)
        f.close()
    except:
        print('Unable to write config')

