import pexpect

child = pexpect.spawn("sudo hcitool lescan")
child.logfile = open("./scanlog", "w")