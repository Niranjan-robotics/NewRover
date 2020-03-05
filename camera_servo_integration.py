# the PCA9685 module.
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import motors
import servo
import objectdetection as obj
import subprocess

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

camera_view =''
tf_in=''

#============== usage ==========
#while running this run some publishing program like servo / classifyimageoncamera.py

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    client.subscribe("test_servo")
    client.subscribe("test_objectdetection")

def on_message(client, userdata, msg):
    global data
    global xCord
    global avgX
    global yCord
    global avgY
    global tf_name
    global tf_xPos
    global tf_yPos
    global action
    global camera_view
    global tf_face_size
    global avgFace
    global face_array
    global avgMovementX
    global face_growth
    global movementX
    global motor_direction
    global start_face_distance
    global face_move
    global currentDetection
    global start_face_needed
    global startTime
    global startTimeCup
    global distance
    global distanceString
    global hotwordTime
    global firstRun
    global needToSleep
    global voiceString
    global subprocess_id
    
    tf_in = (str(msg.payload))
    
    if (tf_in.find("objectdetection:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        face_move = tf_in[(pos1+1):(length)]  # this will give you voice command
        camera_view = face_move=face_move.replace("'","")
        print(camera_view)

        
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)

def runB():
    #client = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    #client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    t2 = Thread(target = runB)
    t2.setDaemon(True)
    t2.start()
    
    try:
        while True:
            if (camera_view.find('Niranjan:') != -1):
                print("Object found is  : " + str(camera_view))
                subprocess.Popen(['mpg123', '-q', '/home/pi/projects/NewRover/snowboy/resources/Niranjan.mp3'])
            if (camera_view.find('Smitha') != -1):
                print("Object found is  : " + str(camera_view))
                subprocess.Popen(['mpg123', '-q', '/home/pi/projects/NewRover/snowboy/resources/Smitha.mp3'])
            if (camera_view.find('Rohan') != -1):
                print("Object found is  : " + str(camera_view))
                subprocess.Popen(['mpg123', '-q', '/home/pi/projects/NewRover/snowboy/resources/Rohan.mp3'])
            if (camera_view.find('Havish') != -1):
                print("Object found is  : " + str(camera_view))
                subprocess.Popen(['mpg123', '-q', '/home/pi/projects/NewRover/snowboy/resources/havish.mp3'])                                
            camera_view= ''
            tf_in=''
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        motors.stopThere()
        GPIO.cleanup()
        client.disconnect()
