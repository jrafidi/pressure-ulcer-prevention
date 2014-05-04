import subprocess

p = subprocess.Popen(["hcitool", "lescan"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
while(True):
  retcode = p.poll() #returns None while subprocess is running
  line = p.stdout.readline()
  yield line
  if(retcode is not None):
    break