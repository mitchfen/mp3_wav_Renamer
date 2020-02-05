# this requires that sox be installed in order for the "play" command to be understood
'''
TODO
I need to loop through files[] and use regex to add \ before spaces
    like /home/mitch/documents\ folder/song.mp3
Then I need to set a timeout so it stops playing after 15 seconds
    add a button to extend playtime?


'''
import os
import subprocess
from pathlib import Path

files = []
#folders = []
for (path, dirnames, filenames) in os.walk('/home/mitch/Music'):
    #folders.extend(os.path.join(path, name) for name in dirnames)
    files.extend(os.path.join(path, name) for name in filenames)

# for debugging
print(files)
os.system("play " + files[0])

# A way to run bash commands -- technically os.system is deprecated
#bashCommand = ""
#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
#output, error = process.communicate()