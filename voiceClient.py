# Import necessary libraries.
from time import sleep
from threading import Thread 
import subprocess
from subprocess import call
from subprocess import Popen, PIPE
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

# Define pin constants
firstRun = True
listening = False


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    global firstRun
    global listening
    
    tf_in = (str(msg.payload))
    
    if (tf_in.find("voice: start recording") != -1):
        if (tf_in.find("speech:") != -1):
            print("Ready for speech")
        elif(listening == False):
            length = len(tf_in)
            pos1 = tf_in.find(':')  # split up the input string
            listening = True #hold for listening audio.
            speechString = tf_in[(pos1+1):(length)]  # this will give you the width of the person
            speechString=distanceString.replace("'","")
            print(speechString)
        
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)

def runB():
    #client = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    #client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
 
if __name__ == '__main__':
    t2 = Thread(target = runB)
    t2.setDaemon(True)
    t2.start()
    try:
        while True:
            firstRun == False
            if (listening == True):
                print("I am Listening")
                #vMsg = subprocess.run(["python3", "/home/pi/projects/NewRover/snowboy/SpeechToText/speech_to_text.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
                vMsg = Popen(["/home/pi/projects/NewRover/runSpeechtoText.sh"], shell = True)
                print(vMsg.stdout)
                listening = False #reset listening mode to false.Ready for next round.
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        client.disconnect()
     
