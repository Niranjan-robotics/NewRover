from subprocess import call
from subprocess import Popen, PIPE

#This main call will run all individual python programs in different terminal one by one

#Don't use and just run one after the other:

#call(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/subscriber.py"])
#call(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/publisher1.py"])
#call(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/publisher2.py"])

#If you don't want them to wait for the process to finish before starting the next use Popen:

#This will not open all terminals seperately.Just one main terminal will display
#Popen(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/subscriber.py"])
#Popen(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/publisher1.py"])
#Popen(["python3", "/home/pi/MyFolders/MQTT/basics-mqtt/publisher2.py"])

#to run python program without launching terminal(in background) and get output.
#bot1 = subprocess.run(["python3", "/home/pi/projects/NewRover/snowboy/SpeechToText/speech_to_text.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
#print(bot1.stdout)

#This will physicall open terminals seperately
edit1 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/roverMainScript.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
edit2 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/distance.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
edit3 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/voiceClient.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
edit4 = Popen(["/home/pi/projects/NewRover/snowboy/runHotword.sh"], shell = True)
#edit5 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/servo.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
edit6 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/objectdetection.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)

