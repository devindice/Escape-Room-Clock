configFile = 'config.json'
import pathlib,json
appPath = str(pathlib.Path(__file__).parent.resolve()) + '/'

def read():
    try:
        with open(f'{appPath}{configFile}') as f:
            data = f.read()
        config = json.loads(data)
    except:
        print("Config does not exist, creating")
        config = {'ticksFullRotation':0,'style':'interleave','currentHr':12,'currentMn':0,'resetHr':12,'resetMn':0,'limitRotationHr':0,'limitRotationMn':0,'triggerHr':1,'triggerMn':0,'triggerPin':37,'triggerDelay':3,'triggerDuration':0.25,'movementDelay':0.25,'movemnentRotation':'full','movementSnap':True,'mqttEnable':True,'mqttBroker':'192.168.1.100','mqttTopicIn':'/pi/clock/in','mqttTopicOut':'/pi/clock/out','autoResetSeconds':300,'reduceDrift':True,'mode':'run','calibrateMethod':4,'autoUpdate':True,'buttonHrFwPin':32,'buttonHrRvPin':36,'buttonMnFwPin':38,'buttonMnRvPin':40}
        write(config)    
    return config

def write(config):
    try:
        f = open(f'{appPath}{configFile}',"w")
        json.dump(config,f)
        f.close()
    except:
        print('Unable to write config')

