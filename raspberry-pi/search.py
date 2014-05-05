import os
from subprocess import Popen, PIPE
from main import *

def findSensorTags():
    addresses = []
    os.system('bash hcireset.sh')
    proc = Popen(["stdbuf -o 0 hcitool lescan"], stdout=PIPE, bufsize=1, shell=True) # start process
    for line in iter(proc.stdout.readline, b''): # read output line-by-line
        if 'SensorTag' in line:
            addresses.append(line.split(' ')[0])
        if len(addresses) >= NUM_TAGS:
            break
    proc.kill()
    return addresses
