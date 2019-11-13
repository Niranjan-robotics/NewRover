from subprocess import call
from subprocess import Popen, PIPE

edit3 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/voiceClient.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
edit4 = Popen(["/home/pi/projects/NewRover/snowboy/runHotword.sh"], shell = True)
edit3 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/subscriber.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)



