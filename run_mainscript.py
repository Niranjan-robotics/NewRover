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


#This will physicall open terminals seperately
bot1 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/RoverWithoutMqtt/roverMainScript.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
bot2 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/RoverWithoutMqtt/distance.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
