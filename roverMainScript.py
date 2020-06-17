# the PCA9685 module.
from time import sleep
from threading import Thread
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import motors
import servo
import objectdetection as obj
import re

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

def getStringBetween(strA,strB,searchString):
    import re
    formS=str.format("{0}(.*){1}",strA,strB)
    result = re.search(formS, searchString)
    return result.group(1)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    client.subscribe("test_servo")
    client.subscribe("test_motor")
    client.subscribe("test_voice")
    client.subscribe("test_objectdetection")
 
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
    print("****************payload********* " + tf_in )
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

    if (tf_in.find("person:") != -1):
        
        # face_move = tf_in[(pos1+1):(length)]  # this will give you voice command
        # camera_view = face_move=face_move.replace("'","")
        startTime = time.time()
        length = len(tf_in)
        pos = tf_in.split(':')[1].split('@')  # split up the input string
        width=int(pos[0]) # this will give you the width of the person
        height=int(pos[1]) # this will give you the height of the person
        pos3=int(pos[2])
        pos4=int(pos[3])
        startX=int(pos[4])
        print(pos)
        # pos1 = getStringBetween(":",";",str(tf_in))
        # pos2 = getStringBetween(";","@",str(tf_in))
        # pos3 = getStringBetween("@","#",str(tf_in))
        # pos4 = getStringBetween("#","$",str(tf_in))
        
        print("*********** width ************" + str(width))
        # tf_face_size = width * height
        # face_array[2] = face_array[1]
        # face_array[1] = face_array[0]
        # face_array[0] = tf_face_size
        # avgFace = face_array[2] + face_array[1] + face_array[0]
        # avgFace = avgFace / 3.0
        #------------nir  perform tracking here using co-ordinates --------------
        center = 320 # this is fixed based on current resolution if any change adjust the value
        
        x_medium = int((startX + startX + width) / 2)
        print("************** startX  " + str(startX))
        print("************** x_medium " + str(x_medium))
        print("************** position " + str(position))
        
        coordinates = str.format("******* x_medium : {0} position : {1} startX : {2}",str(x_medium),str(position),str(startX))
        print(coordinates)
        
        # Move servo motor
        if x_medium < center -30:
            position += (2)
            c= str.format("center:{0}   x_medium: {1}  Position: {2}",str(center),str(x_medium) ,str(position))
            print(c)
        elif x_medium > center + 30:
            position -= (2)
            c= str.format("center:{0}   x_medium: {1}  Position: {2}",str(center),str(x_medium) ,str(position))
            print(c)
        # servo.pwm.set_pwm(1, 0, position)
        servo.scanLeftRight(position)
        # ---------- end of screen postion --------
        print(camera_view)
        print(avgX)
        print(avgFace)
        print(tf_xPos)
        print(tf_yPos)
        tf_xPos = float(tf_in[(pos3 + 1):pos4])
        tf_yPos = float(tf_in[(pos4+1):length])
        yCord[2] = yCord[1]
        yCord[1] = yCord[0]
        yCord[0] = tf_yPos
        avgY = yCord[2] + yCord[1] + yCord[0]
        avgY = avgY / 3.0
        xCord[2] = xCord[1]
        xCord[1] = xCord[0]
        xCord[0] = tf_xPos
        avgX = xCord[2] + xCord[1] + xCord[0]
        avgX = avgX / 3.0
        print("avg size ", avgFace, "xpos ", tf_xPos, "ypos ", tf_yPos,)
        
        if start_face_needed == True:
            start_face_distance = tf_face_size
            start_face_needed = False
       
        if avgX == 0:
            motor_direction == "unsure"
        elif avgX>470:
            motor_direction = "left"
        elif avgX<170:
            motor_direction = "right"
        elif avgX <470 and avgX >170:
            motor_direction = "neither"
        if (currentDetection == "face"):
            if (avgFace > (start_face_distance + 8000)): #100 is a filter
                face_move = "further"
            elif (avgFace < (start_face_distance -8000)):
                face_move = "closer"
            else:
                face_move = ""
        t = 0
    
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
            currentDetection="face"
            if (currentDetection == "face"):
                # if (time.time() > startTime + 10):
                    # motor_direction = "unsure"
                if (motor_direction == "left"):
                    print ("R")
                    try:
                        motors.turnRight()
                    except:
                        print("")
                elif (motor_direction == "right"):
                    print ("L")
                    try:
                        motors.turnLeft()
                    except:
                        print("")
                    #sleep(0.3)
                    #motor_direction = ""
                elif (motor_direction == "unsure" and firstRun == False):
                    print("rotating")
                    servo.scanLeftRight(500)
                else:
                    print("N")
                    if (face_move == 'further'):
                        print("MAIN further")
                        try:
                            motors.goForward()
                        except:
                            print("")

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
            #if (voiceString.find('face') != -1) or (voiceString.find('coco') != -1):
            #    print("launching object detection")
            #    obj.main()
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        motors.stopThere()
        GPIO.cleanup()
        client.disconnect()

