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
import logging
import logging.config
import yaml

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
currentMotorAction = "stop"
motor_direction = "unsure"
action = True

start_face_distance = 0
start_face_needed = False

currentDetection = "face"
minDistance = 25
startTime = time.time()
startTimeCup = time.time()
distanceString = ''
voiceString = 'speech:stop'
distance = 0.0
needToSleep = False
firstRun = True

positionX = 410
positionY = 400

left= False
right= False
top= False
down = False
eleft= False
eright= False
etop= False
edown = False
#==================Motor connect======================================

motors.motorSetup()
servo.setFreq(50)
# This command will trigger starting point message
motors.stopThere()

logging.basicConfig(filename='/home/pi/projects/NewRover/consoleLog.log', filemode='w',level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

def logInfo(msg):
    logger.info(msg)

logInfo("this is test log")
  
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
    global positionX
    global positionY
    global logger
    global left
    global right
    global top
    global down
    global eleft
    global eright
    global etop
    global edown
    global currentMotorAction
    
    #turn left right values
    hori_left_max= 475   #left
    hori_straight= 420  #Center
    hori_right_max= 300   #right

    #turn left right values
    vert_up_max= 200 ##pwm.set_pwm(0, 100, 200)
    vert_straight_= 350  #pwm.set_pwm(0, 0, 420)
    vert_down_max= 375  #pwm.set_pwm(0, 50, 450)

    
    tf_in = (str(msg.payload))
    # print("****************payload********* " + tf_in )
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
        logInfo("***********************")
        pos = tf_in.split(':')[1].split('@')  # split up the input string
        logInfo(pos)
        pos1=int(pos[0].replace("'",""))
        pos2=int(pos[1].replace("'",""))
        # print(pos)
        # width=int(pos[0]) # this will give you the width of the person
        # height=int(pos[1]) # this will give you the height of the person
        pos3=float(pos[2].replace("'",""))
        pos4=float(pos[3].replace("'",""))
        startX=int(pos[4].replace("'",""))
        startY=int(pos[5].replace("'",""))
            
        width = pos1
        height = pos2
        tf_face_size = width * height
        face_array[2] = face_array[1]
        face_array[1] = face_array[0]
        face_array[0] = tf_face_size
        avgFace = face_array[2] + face_array[1] + face_array[0]
        avgFace = avgFace / 3.0
        # print(tf_in)
        # 9feet distance from face = 1706  (start greater than 100)
        # < 1 feet distance = 768080 to 838080  (stop greater than 700000)
        face_axis = str.format("******* width : {0} height : {1} tf_face_size : {2} avgFace :{3}",str(width),str(height),str(tf_face_size),str(avgFace))
        # print(face_axis)
        
        centerX = 640 # this is fixed based on current resolution (1280/720) if any change adjust the value
        centerY = 360
        
        x_medium = int(startX) + int(width) / 2
        y_medium = int(startY) + int(height) / 2
        
        coordinatesX = str.format("******* x_medium : {0} centerx : {2} positionX : {1} ",str(x_medium),str(positionX),str(centerX))
        coordinatesY = str.format("******* y_medium : {0} cemtrY : {2} positionY : {1}",str(y_medium),str(positionY),str(centerY))
        # print(coordinatesX)
        # print(coordinatesY)


        # Move servo motor left/right
        if (positionX < hori_left_max) and (positionX > hori_right_max) and x_medium < centerX -30:
            positionX += (2)
            servo.scanLeftRight(positionX)  
            motor_direction = "left"
        elif (positionX < hori_left_max) and (positionX > hori_right_max) and x_medium > centerX + 30:
            positionX -= (2)
            motor_direction = "right"
            servo.scanLeftRight(positionX)

        # Move servo motor
        if (positionY < vert_down_max) and (positionY > vert_up_max) and (y_medium < centerY -30):
            positionY -= (2)
            servo.scanUpDown(positionY)
        elif (positionY < vert_down_max) and (positionY > vert_up_max) and (y_medium > centerY + 30):
            positionY += (2)
            servo.scanUpDown(positionY)
        elif (positionY >= vert_down_max) or (positionY <= vert_up_max):
            positionY = vert_straight_
            time.sleep(0.2)
        
        # servo.scanLeftRight(positionX)    
        # servo.scanUpDown(positionY)
        
        # ---------- end of screen postion --------

        tf_xPos = float(pos2)
        tf_yPos = float(pos3)
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
        # elif avgX>500:
            # motor_direction = "left"
        # elif avgX<100:
            # motor_direction = "right"
        # # elif avgX <470 and avgX >170:
            # motor_direction = "neither"
        if (currentDetection == "face"):
            if (avgFace > (start_face_distance + 8000)): #100 is a filter
                face_move = "further"
            elif (avgFace < (start_face_distance -8000)):
                face_move = "closer"
            else:
                face_move = ""
        print(motor_direction)
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
                if (time.time() > startTime + 10):
                    motor_direction = "unsure"
                if (motor_direction == "left"):
                    print ("R")
                    try:
                        motors.turnLeft()
                        time.sleep(3)
                        motors.stopThere()
                        currentMotorAction = "stop"                        
                    except:
                        print("")
                elif (motor_direction == "right"):
                    print ("L")
                    try:
                        motors.turnRight()
                        time.sleep(3)
                        motors.stopThere()
                        currentMotorAction = "stop"
                    except:
                        print("")
                    #sleep(0.3)
                    #motor_direction = ""
                elif (motor_direction == "unsure" and firstRun == False):
                    print("rotating")
                    motors.turnRight()
                    time.sleep(6)
                    motors.stopThere()
                    currentMotorAction = "stop"
                else:
                    print("N")
                    if (face_move == 'further'):
                        print("MAIN further")
                        try:
                            if(currentMotorAction != "forward"):
                                motors.goForward()
                                time.sleep(0.2)
                                currentMotorAction = "forward"                            
                        except:
                            print("")
                    elif(face_move =='closer'):
                        print("MAIN closer")
                        try:
                            if(currentMotorAction != "stop"):
                                motors.stopThere()
                                currentMotorAction="stop"
                        except:
                            print("")
                    else:
                        print('N')
                        try:
                            if(currentMotorAction != "stop"):
                                motors.stopThere()
                                currentMotorAction="stop"
                        except:
                            print("")

            # if (distance < minDistance):
                # print("Object is little close : " + str(distance))
                # motors.stopThere()
            # if (voiceString.find('stop') != -1 & face_move.find('stop') == -1):
                # motors.stopThere()
            # if (voiceString.find('forward') != -1 &  face_move.find('forward') == -1):
                # motors.goForward()
            # if (voiceString.find('backward') != -1 & face_move.find('backward') == -1):
                # motors.goBackward()
            # if (voiceString.find('right') != -1):
                # motors.turnRight()
            # if (voiceString.find('left') != -1):
                # motors.turnLeft()
            # if (voiceString.find('up') != -1 & face_move.find('up') == -1):
                # servo.lookUp()
            # if (voiceString.find('down') != -1 & face_move.find('down') == -1):
                # servo.lookDown()
            # if (voiceString.find('straight') != -1 & face_move.find('straight') == -1):
                # servo.lookStraight()
            #if (voiceString.find('face') != -1) or (voiceString.find('coco') != -1):
            #    print("launching object detection")
            #    obj.main()
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        motors.stopThere()
        GPIO.cleanup()
        client.disconnect()
