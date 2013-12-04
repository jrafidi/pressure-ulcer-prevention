import serial
import math

ACCEL_ZERO = 330
ALPHA = 0.2

SLEEP_AXIS = 1

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

def findAngle(vector1, vector2):
    '''
    Repeatedly rotate both vectors by some small angle,
    calculating error from what we want at each step.
    Return list of 2 vectors that are our zero angle vectors.
    '''

    error = 1000000000
    best_theta = 0.0

    start_angle = -1 * math.pi / 2.0
    end_angle = math.pi / 2.0
    increment = math.pi / 1000.0

    for theta in frange(start_angle, end_angle, increment):
        cs = math.cos(theta)
        sn = math.sin(theta)

        rot1x = vector1[0]*cs - vector1[1]*sn
        rot1y = vector1[0]*sn + vector1[1]*cs

        rot2x = vector2[0]*cs - vector2[1]*sn
        rot2y = vector2[0]*sn + vector2[1]*cs

        current_error = abs((rot1x + rot2x) + (rot1y - rot2y))

        if current_error < error:
            error = current_error
            best_theta = theta
        #else:
        #    break
    return best_theta

def findZeroVectors(vector1, vector2):
    '''
    Repeatedly rotate both vectors by some small angle,
    calculating error from what we want at each step.
    Return list of 2 vectors that are our zero angle vectors.
    '''
    
    error = 10000
    best_zero_vector_1 = []
    best_zero_vector_2 = []

    start_angle = -1 * math.pi / 2.0
    end_angle = math.pi / 2.0
    increment = math.pi / 1000.0

    for theta in frange(start_angle, end_angle, increment):
        cs = math.cos(theta)
        sn = math.sin(theta)

        rot1x = vector1[0]*cs - vector1[1]*sn
        rot1y = vector1[0]*sn + vector1[1]*cs

        rot2x = vector2[0]*cs - vector2[1]*sn
        rot2y = vector2[0]*sn + vector2[1]*cs

        current_error = abs((rot1x + rot2x)) + abs((rot1y - rot2y))

        if current_error < error:
            error = current_error
            best_zero_vector_1 = [rot1x, rot1y]
            best_zero_vector_2 = [rot2x, rot2y]
        else:
            break
    return [best_zero_vector_1, best_zero_vector_2]
        
def normalizeVector(vector):
    total = 0
    for val in vector:
        total = total + val**2
    mag  = total**0.5

    norm = []
    for val in vector:
        norm.append(val / mag)
    return norm

# Running average we are measuring
avg = None

# Two vectors such that <x1,z1> = <x2, z2>
zero_vector_1 = []
zero_vector_2 = []

def calculateAngle(vals):
    global avg
    global zero_vector_1
    global zero_vector_2

    x1 = int(vals[0]) - ACCEL_ZERO
    z1 = int(vals[2]) - ACCEL_ZERO

    x2 = int(vals[3]) - ACCEL_ZERO
    z2 = int(vals[5]) - ACCEL_ZERO

    vector1 = [x1, z1]#normalizeVector([x1, z1])
    vector2 = [x2, z2]#normalizeVector([x2, z2])

    # Find the zero vectors if we haven't already
    #if len(zero_vector_1) == 0:
    #    [zero_vector_1, zero_vector_2] = findZeroVectors(vector1, vector2)

    # Calculate the angle and average
    #[x1_0, z1_0] = zero_vector_1

    # TODO: figure out how to avoid this -1 here.
    # TODO: understand coordinate frames wrt patient better
    #product = -1 * vector1[0]*x1_0 + vector1[1]*z1_0
    #theta = math.acos(product) * (180/math.pi)
    
    theta = findAngle(vector1, vector2)
    theta = theta * (180/math.pi)

    #if vector1[0] < 0:
    #    theta = -1 * theta

    if avg == None:
        avg = theta
    else:
        avg = (ALPHA) * theta + (1.0 - ALPHA) * avg
    return avg

def calculateSleeping(vals):
    val = int(vals[6 + SLEEP_AXIS]) - ACCEL_ZERO
    if val < -40:
        return False 
    else:
        return True
