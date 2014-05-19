import math

SLEEP_AXIS_SIT = 1
SLEEP_AXIS_LAY = 2

def frange(x, y, jump):
    while x <= y:
        yield x
        x += jump
        
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

def calculateAngle(leftAccel, rightAccel):
    x1 = leftAccel[0]
    z1 = -1*leftAccel[2]

    x2 = rightAccel[0]
    z2 = -1*rightAccel[2]

    vector1 = normalizeVector([x1, z1])
    vector2 = normalizeVector([x2, z2])
    
    theta = findAngle(vector2, vector1)
    theta = -1 * theta * (180/math.pi)
    return theta

def calculateSleeping(centerAccel):
    val_sit = abs(centerAccel[SLEEP_AXIS_SIT])
    val_lay = abs(centerAccel[SLEEP_AXIS_LAY])
    if val_sit > val_lay:
        return False 
    else:
        return True
