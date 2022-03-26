import app.logger as logger
import app.motor as motor

def time(parameters,add_subtract,unit):
    if unit == 'hour':
        h = parameters.get('currentHr')
        if add_subtract == 'add':
            logger.log.info('Add 1 hour')
            #motor.clock(parameters,'cw', 'hour', 1)
            h += 1
            if h > 12:
                h = 1
        elif add_subtract == 'subtract':
            logger.log.info('Subtract 1 hour')
            #motor.clock(parameters,'ccw', 'hour', 1)
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
            #motor.clock(parameters,'cw', 'minute', minute)

            m += minute
            if m > 59:
                m = 0 
        elif add_subtract == 'subtract':
            logger.log.info('Subtract %s minute(s)' %(minute))
            #motor.clock(parameters,'ccw', 'minute', minute)
            m -= int(parameters.get('movementMinuteStep'))
            if m < 0:
                m = 60 - int(parameters.get('movementMinuteStep'))
        else:
            logger.log.error('Unknown option for "add_subtract": %s, Only accepts "add" or "subtract"' %(add_subtract))
        parameters['currentMn'] = m
    else:
        logger.log.error('Unknown option for "unit": %s, Only accepts "hour" or "minute"' %(unit))

# Changes


def add_subtract(hour_minute,add_subtract,val1,val2):
    logger.log.debug('Calculation: %sing %s to/from %s' %(add_subtract, val2, val1))
    # Set limits
    if hour_minute == 'hour':
        limit = 12
    elif hour_minute == 'minute':
        limit = 60

    # Addition
    if add_subtract == 'add':
        result = float(val1) + float(val2)
        if result > limit:
            result -= limit
    
    # Subtraction
    elif add_subtract == 'subtract':
        result = float(val1) - float(val2)
        if result <= 0:
            result += limit

    # Set to 0 if value is minutes
    if hour_minute == 'minute':
        if result == limit:
            result = 0
    logger.log.debug('Calculation: The new value is: %s' %(result))
    return result
    

def jump(hour_minute,current,target):
    # Set limits
    if hour_minute == 'hour':
        limit = 12
    elif hour_minute == 'minute':
        limit = 60
    
    # Get half way
    half = limit / 2

    # Calculate
    result = float(current) - float(target)

    # No negative values
    if result < 0:
        result = limit + result

    # If more than half way, go the other direction
    if result > half:
        result = float(target) - float(current)
        # No negative values
        if result < 0:
            result = limit + result
        result = ('cw', result)
    else:
        result = ('ccw', result)
    return result


























