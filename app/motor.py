import app.logger as logger
import app.clock as clock
import app.multithread as multithread
from adafruit_motorkit import MotorKit
kit = MotorKit()
from adafruit_motor import stepper
import time


@multithread.background
def listener(globalParameters):
    global parameters
    parameters = globalParameters
    try:
        while True:
            motors(parameters,'hour')
            motors(parameters,'minute')
            time.sleep(0.1)
    except:
        logger.log.critical("Listener Crashed", exc_info=True)

def motors(parameters,hour_minute):
    # Get parameters
    style = parameters.get('style')
    # What parameter should be pulled
    if hour_minute == 'hour':
        unit = 'Hr'
    elif hour_minute == 'minute':
        unit = 'Mn'
    # Get the current position
    current = parameters.get('current' + unit)

    # Determine mode and set the target
    mode = parameters.get('mode')
    if mode == 'gameTimer':
        target = parameters.get('default' + unit)
    elif mode == 'play':
        target = parameters.get('set' + unit)
    elif mode == 'calibrate':
        if hour_minute == 'hour':
            target = 12
        elif hour_minute == 'minute':
            target = 0

    # Get motor
    motor = parameters.get('motor' + unit)

    # Get movement
    cw_ccw,count = clock.jump(hour_minute,current,target)

    # Calculate ticks
    fullSteps = parameters.get('ticksFullRotation')
    if hour_minute == 'hour':
        multiplier = fullSteps / 12
    elif hour_minute == 'minute':
        multiplier = fullSteps / 60
    steps = count * multiplier

    if cw_ccw == 'cw':
        direction = 'clockwise'
    elif cw_ccw == 'ccw':
        direction = 'counterclockwise'

    # Move Motor
    if count > 0:
        logger.log.info('Moving %s hand %s %s step(s)' %(hour_minute, direction, count))
        motorControl(motor,cw_ccw, style, steps)

        # Set current value
        parameters['current' + unit] = target

def motorControl(motor,cw_ccw, style, steps):
    if cw_ccw == 'cw':
        direction = stepper.FORWARD
    elif cw_ccw == 'ccw':
        direction = stepper.BACKWARD
    else:
        print('unknown')
    if style == 'interleave':
        style=stepper.INTERLEAVE
        steps = int(steps / 8)
    elif style == 'single':
        steps = int(steps / 16)
        style=stepper.SINGLE
    elif style == 'double':
        style=stepper.DOUBLE
        steps = int(steps / 16)
    elif style == 'micro':
        style=stepper.MICROSTEP
        steps = steps
    else:
        print('unknown2')
    for i in range(steps):
        if motor == 'motor2':
            kit.stepper1.onestep(direction=direction, style=style)
        elif motor == 'motor1':
            kit.stepper2.onestep(direction=direction, style=style)

