import sys
import subprocess
from time import sleep


with open('requirements.txt') as f:
    lines = f.readlines()
# implement pip as a subprocess:
for line in lines:
    print('Installing '+line)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', line])
    sleep(0.5)
    print('Successfully Installed '+line)
    sleep(0.5)

print('\nAll DONE!')