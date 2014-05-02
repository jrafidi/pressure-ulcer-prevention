import math

ACCEL_ZERO = 0
Z_ZERO = 0
Z_OFFSET = 0

SLEEP_AXIS_SIT = 0
SLEEP_AXIS_LAY = 2

def frange(x, y, jump):
    while x <= y:
        yield x
        x += jump

def findAngle(vector1, vector2):
    error = 1000000000
    best_theta = 1000

    start_angle = -1 * math.pi / 2.0
    end_angle = math.pi / 2.0
    increment = math.pi / 1000.0

    for theta in frange(start_angle, end_angle, increment):
        [rot1x, rot1y] = rotateVector(vector1, theta)
        [rot2x, rot2y] = rotateVector(vector2, theta)
        if rot1y > 0 and rot2y > 0:
            continue

        current_error = abs((rot1x + rot2x) + (rot1y - rot2y))
        if current_error < error:
            error = current_error
            best_theta = theta

    return best_theta
        
def rotateVector(vector, theta):
    cs = math.cos(theta)
    sn = math.sin(theta)
    rotX = vector[0]*cs - vector[1]*sn
    rotY = vector[0]*sn + vector[1]*cs
    return [rotX, rotY]

def normalizeVector(vector):
    total = 0
    for val in vector:
        total = total + val**2
    mag  = total**0.5

    norm = []
    for val in vector:
        norm.append(val / mag)
    return norm

def calculateAngle(vals):
    global avg

    x1 = int(vals[0]) - ACCEL_ZERO
    z1 = int(vals[2]) - Z_ZERO

    x2 = -1 * (int(vals[3]) - ACCEL_ZERO)
    z2 = int(vals[5]) - Z_ZERO - Z_OFFSET

    vector1 = normalizeVector([x1, z1])
    vector2 = normalizeVector([x2, z2])
    
    theta = findAngle(vector1, vector2)
    theta = -1 * theta * (180/math.pi)
    return theta

def calculateSleeping(vals):
    val_sit = abs(int(vals[6 + SLEEP_AXIS_SIT]) - ACCEL_ZERO)
    val_lay = abs(int(vals[6 + SLEEP_AXIS_LAY]) - ACCEL_ZERO)
    if val_sit > val_lay:
        return False 
    else:
        return True

if __name__ == '__main__':
    print rotateVector([-1,0], math.pi/4.0)
    print "Testing flat accels from -90 to 90..."
    for theta in range(-90, 90, 1):
        rad = theta * (math.pi / 180.0)
        inp = [-1 * math.sin(rad), 0, -1 * math.cos(rad), -1 * math.sin(rad), 0, -1 * math.cos(rad)]
        result = calculateAngle(inp)
        if abs(theta - result) > 1:
            print "TEST FAILED ON THETA = " + str(theta)
            print "RETURNED: " + str(result)
    print "Testing flat accels complete."

    print "Testing 90deg accels from -90 to 90..."
    for theta in range(-90, 90, 1):
        rad = theta * (math.pi / 180.0)
        [rot1x, rot1y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], math.pi/2.0)
        [rot2x, rot2y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], -1 * math.pi/2.0)
        inp = [rot1x, 0, rot1y, rot2x, 0, rot2y]
        result = calculateAngle(inp)
        if abs(theta - result) > 1:
            print "TEST FAILED ON THETA = " + str(theta)
            print "RETURNED: " + str(result)
    print "Testing 90deg accels complete."

    print "Testing 45deg accels from -90 to 90..."
    for theta in range(-90, 90, 1):
        rad = theta * (math.pi / 180.0)
        [rot1x, rot1y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], math.pi/4.0)
        [rot2x, rot2y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], -1 * math.pi/4.0)
        inp = [rot1x, 0, rot1y, rot2x, 0, rot2y]
        result = calculateAngle(inp)
        if abs(theta - result) > 1:
            print "TEST FAILED ON THETA = " + str(theta)
            print "RETURNED: " + str(result)
    print "Testing 45deg accels complete."

    print "Testing 30deg accels from -90 to 90..."
    for theta in range(-90, 90, 1):
        rad = theta * (math.pi / 180.0)
        [rot1x, rot1y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], math.pi/6.0)
        [rot2x, rot2y] = rotateVector([-1 * math.sin(rad), -1 * math.cos(rad)], -1 * math.pi/6.0)
        inp = [rot1x, 0, rot1y, rot2x, 0, rot2y]
        result = calculateAngle(inp)
        if abs(theta - result) > 1:
            print "TEST FAILED ON THETA = " + str(theta)
            print "RETURNED: " + str(result)
    print "Testing 30deg accels complete."
