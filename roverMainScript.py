# the PCA9685 module.
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import motors
import servo

MQTT_SERVER = "localhost"
MQTT_PATH = "test_channel"

data = "no data"
xCord = [0,0,0]
avgX = 0.0

avgY = 0.0
yCord = [1,2,3]

face_array = [0,0,0]
avgFace =0

face_growth = [0,0,0]
face_move = ""

tf_name = ""
tf_xPos = 0
tf_yPos = 0
tf_face_size = 0;
avgMovementX = 400
movementX = [1,2,3]
motor_direction = "unsure"
action = False

start_face_distance = 0
start_face_needed = False

currentDetection = "face"
minDistance = 25
startTime = time.time()
startTimeCup = time.time()
distanceString = ''
voiceString = ''
distance = 0.0
needToSleep = False
firstRun = True


#==================Motor connect======================================

motors.motorSetup()
servo.setFreq(50)
servo.lookDown()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    client.subscribe("test_servo")
    client.subscribe("test_motor")
    client.subscribe("test_voice")
 
# The callback for when a PUBLISH message is received from the server.
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
    
    if (tf_in.find("coco distance:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        distanceString = tf_in[(pos1+1):(length)]  # this will give you distance to object
        distanceString=distanceString.replace("'","")
        distance = int(distanceString)
    if (tf_in.find("speech:") != -1):
        print(voiceString)
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        voiceString = tf_in[(pos1+1):(length)]  # this will give you voice command
        voiceString=voiceString.replace("'","")

    if (tf_in.find("current status:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        face_move = tf_in[(pos1+1):(length)]  # this will give you voice command
        motor_direction = face_move=face_move.replace("'","")

        
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
            firstRun == False
            currentDetection="distance"
            if (distance < minDistance):
                print("Object is little close : " + str(distance))
                motors.stopThere()
            if (voiceString.find('stop') != -1 & face_move.find('stop') == -1):
                motors.stopThere()
            if (voiceString.find('forward') != -1 &  face_move.find('forward') == -1):
                motors.goForward()
            if (voiceString.find('backward') != -1 & face_move.find('backward') == -1):
                motors.goBackward()
            if (voiceString.find('right') != -1):
                motors.turnRight()
            if (voiceString.find('left') != -1):
                motors.turnLeft()
            if (voiceString.find('up') != -1 & face_move.find('up') == -1):
                servo.lookUp()
            if (voiceString.find('down') != -1 & face_move.find('down') == -1):
                servo.lookDown()
            if (voiceString.find('straight') != -1 & face_move.find('straight') == -1):
                servo.lookStraight()
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        motors.stopThere()
        GPIO.cleanup()
        client.disconnect()

