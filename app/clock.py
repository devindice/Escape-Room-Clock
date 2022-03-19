import app.config as config

def time(add_subtract,unit):
    settings = config.read()
    print(add_subtract,unit)
    if unit == 'hour':
        h = settings.get('currentHr')
        if add_subtract == 'add':
            h += 1
            if h > 12:
                h = 1
        elif add_subtract == 'subtract':
            h -= 1
            if h < 1:
                h = 12
        else:
            print('unknown function')
        settings['currentHr'] = h

    elif unit == 'minute':
        m = settings.get('currentMn')
        if add_subtract == 'add':
            m += int(settings.get('movementMinuteStep'))
            if m > 59:
                m = 0 
        elif add_subtract == 'subtract':
            m -= int(settings.get('movementMinuteStep'))
            if m < 0:
                m = 60 - int(settings.get('movementMinuteStep'))
        else:
            print('unknown function')
        settings['currentMn'] = m

    config.write(settings)
