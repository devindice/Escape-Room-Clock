import app.logger as logger
import app.motor as motor

def time(parameters,add_subtract,unit):
    if unit == 'hour':
        h = parameters.get('currentHr')
        if add_subtract == 'add':
            logger.log.info('Add 1 hour')
            motor.clock('cw', 'hour', 1)
            h += 1
            if h > 12:
                h = 1
        elif add_subtract == 'subtract':
            logger.log.info('Subtract 1 hour')
            motor.clock('ccw', 'hour', 1)
            h -= 1
            if h < 1:
                h = 12
        else:
            logger.log.error('Unknown option for "add_subtract": %s, Only accepts "add" or "subtract"' %(add_subtract))
        parameters['currentHr'] = h

    elif unit == 'minute':
        m = parameters.get('currentMn')
        minute = int(parameters.get('movementMinuteStep'))
        if add_subtract == 'add':
            logger.log.info('Add %s minute(s)' %(minute))
            motor.clock('cw', 'minute', minute)
            m += minute
            if m > 59:
                m = 0 
        elif add_subtract == 'subtract':
            logger.log.info('Subtract %s minute(s)' %(minute))
            motor.clock('ccw', 'minute', minute)
            m -= int(parameters.get('movementMinuteStep'))
            if m < 0:
                m = 60 - int(parameters.get('movementMinuteStep'))
        else:
            logger.log.error('Unknown option for "add_subtract": %s, Only accepts "add" or "subtract"' %(add_subtract))
        parameters['currentMn'] = m
    else:
        logger.log.error('Unknown option for "unit": %s, Only accepts "hour" or "minute"' %(unit))

