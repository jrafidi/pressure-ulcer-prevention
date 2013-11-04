import serial
import math

ACCEL_ZERO = 330
ALPHA = 0.2

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.close()
    ser.open()
    ser.flushInput()

    zero_angle = []
    mag0 = 0
    avg = 0

    while 1:
        vals = ser.readline().strip().split(' ')

        if len(vals) != 3:
            continue
        
        x = int(vals[0]) - ACCEL_ZERO
        z = int(vals[2]) - ACCEL_ZERO
        mag = (x**2 + z**2)**0.5

        x = x / mag
        z = z / mag
        mag = 1

        if len(zero_angle) == 0:
            zero_angle = [x, z]
            mag0 = mag
        
        [x0, z0] = zero_angle
        product = x*x0 + z*z0

        cos_theta = product / (mag * mag0)
        theta = math.acos(cos_theta)

        if x < 0:
            theta = theta * -1

        theta = theta * (180/math.pi)
        avg = (ALPHA) * theta + (1.0 - ALPHA) * avg
        print avg
