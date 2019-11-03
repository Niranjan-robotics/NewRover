# the PCA9685 module.
import Adafruit_PCA9685
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import time 
import RPi.GPIO as GPIO
import time
import servo
import motors

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
distance = 0.0
needToSleep = False
firstRun = True

#==================Motor connect======================================

motors.motorSetup()
#initially stops
#motors.stopThere()

#====================  servo and motor initialize ========================

# servo_look_straight = 376  # Min pulse length out of 4096
# servo_look_right = 170  # Max pulse length out of 4096
# servo_look_left = 600  # Max pulse length out of 4096
# def panStraight():
    # print("look pan straight")
    # servo.setSevoAngle(0,servo_look_straight)
    # time.sleep(0.5)
# def panRight():
    # print("look pan Right")
    # servo.setSevoAngle(0,servo_look_right)
    # time.sleep(0.5)
# def panLeft():
    # print("look pan Left")
    # servo.setSevoAngle(0,servo_look_left)
    # time.sleep(0.5)
    
# def tiltStrainght():
    # print("look tilt straight")
    # servo.setSevoAngle(1,servo_look_straight)
    # time.sleep(0.5)
# def tiltUp():
    # print("look tilt right")
    # servo.setSevoAngle(1,servo_look_right)
    # time.sleep(0.5)
# def tiltDown():
    # print("look tilt left")
    # servo.setSevoAngle(1,servo_look_left)
    # time.sleep(0.5)   
    
# panStraight()     
# panRight()
# panLeft()

# tiltStrainght()
# tiltUp()
# tiltDown()

servo.lookStraight()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    client.subscribe("test_servo")
    client.subscribe("test_motor")
 
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
    
    tf_in = (str(msg.payload))
    
    if (tf_in.find("coco distance:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        #print(pos1)
        distanceString = tf_in[(pos1+1):(length)]  # this will give you the width of the person
        distanceString=distanceString.replace("'","")
        distance = int(distanceString)


        
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
            if (distance > minDistance):
                print("Object is little far : " + str(distance))
                servo.lookStraight()
                motors.goForward()
            if (distance < minDistance):
                print("Object is little close : " + str(distance))
                servo.panRight()
                motors.stopThere()
                motors.turnRight()
                time.sleep(1)
                motors.goForward()
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        motors.stopThere()
        GPIO.cleanup()
        client.disconnect()

