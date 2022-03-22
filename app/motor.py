import app.logger as logger
from adafruit_motorkit import MotorKit
kit = MotorKit()
from adafruit_motor import stepper
import time

def clock(parameters,cw_ccw, hour_minute, count):
    fullSteps = parameters.get('ticksFullRotation')
    stepsMinute = fullSteps / 60
    stepsHour = fullSteps / 12
    motorHr = parameters.get("motorHr")
    motorMn = parameters.get("motorMn")
    style = parameters.get("style")
    movementDelay = parameters.get("movementDelay")
    for i in range(count):
        if hour_minute == 'hour':
            motorControl(motorHr,cw_ccw, style, stepsHour)
        elif hour_minute == 'minute':
            motorControl(motorMn,cw_ccw, style, stepsMinute)
    time.sleep(movementDelay)

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

