import app.logger as logger
from adafruit_motorkit import MotorKit
kit = MotorKit()
from adafruit_motor import stepper
import time

def clock(cw_ccw, hour_minute, count):
    fullSteps = 12000
    stepsMinute = fullSteps / 60
    stepsHour = fullSteps / 12
    if hour_minute == 'hour':
        for i in range(count):
            motorControl('motor1',cw_ccw, 'interleave', stepsHour)
            time.sleep(0.25)
    elif hour_minute == 'minute':
        for i in range(count):
            motorControl('motor2',cw_ccw, 'interleave', stepsMinute)
            time.sleep(0.25)

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

