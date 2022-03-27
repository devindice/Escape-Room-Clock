import app.logger as logger
import app.motor as motor

# Add or Subtract time
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
    
# Calculate a jump to move motor when switching modes or moving to another time.
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
