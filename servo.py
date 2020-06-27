from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import time
import logging
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
MQTT_SERVER = "localhost"
MQTT_PATH = "test_servo"
#----------------Note------------------------- Debug servo issues ---------------
#   $ i2cdetect -y 1
# keep trying with 0/1/2 for few times until 1 return correct values
# this should retun 40 /70 i2c
#  cat /boot/cmdline.txt
#    $lsmod | grep i2c
#==========================================

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

#turn left right values
hori_left_max= 475
hori_straight_= 420
hori_right_max= 150

#turn left right values
vert_up_max= 200 ##pwm.set_pwm(1, 100, 200)
vert_straight_= 350  #pwm.set_pwm(1, 0, 420)
vert_down_max= 375  #pwm.set_pwm(1, 50, 450)


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def setFreq(pwmFreq=50):
    pwm.set_pwm_freq(pwmFreq)
    
def deInitServo():
    pwm.deinti()    
# tild commands    
        
def lookUp90():
    print("Looking up")
    #look 90 degree up
    pwm.set_pwm(1, 100, 200)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: up', hostname=MQTT_SERVER)
    
def lookUp70():
    print("Looking up")
    #look 90 degree up
    #look straigh and up 70 degree
    pwm.set_pwm(1, 100, 300)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: up', hostname=MQTT_SERVER)
    
def lookStraight():
    print("look straight")
    #pwm.set_pwm(1, 100, 300)
    #time.sleep(1)
    pwm.set_pwm(3, 0, 420)
    time.sleep(1)
    pwm.set_pwm(1, 0, 350)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)
    
def lookDownMax():
    print("look down")
    pwm.set_pwm(1, 50, 450)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: down', hostname=MQTT_SERVER)
    time.sleep(1)

def lookLeft():
    print("look left")
    pwm.set_pwm(1, 0, 300)
    time.sleep(1)
    pwm.set_pwm(3, 0, 420)
    time.sleep(1)
    pwm.set_pwm(3, 0, 600)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)

def lookRight():
    print("look right")
    pwm.set_pwm(1, 100, 300)
    time.sleep(1)
    pwm.set_pwm(3, 0, 250)
    time.sleep(1)
    pwm.set_pwm(1, 100, 300)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)

def lookBackRight():
    print("look back")
    pwm.set_pwm(0, 0, 24)
    time.sleep(1)
    pwm.set_pwm(1, 0, 24)
    time.sleep(1)
    #pwm.set_pwm(1, 0, 250)
    time.sleep(1)

#input range to restrict to given coordinates
def scanLeft():
    lookStraight()
    for i in range(hori_straight_,hori_left_max):
        pwm.set_pwm(3, 0, i)
        print(i)
        time.sleep(0.1)

#input range to restrict to given coordinates
def scanRight():
    lookStraight()
    for i in range(hori_right_max):
        pwm.set_pwm(3, 0, hori_straight_ - i)
        print(hori_straight_ - i)
        time.sleep(0.1)
        
#input range to restrict to given coordinates
def scanDown():
    lookStraight()
    for i in range(vert_up_max,vert_down_max):
        pwm.set_pwm(1, 0, i)
        print(i)
        time.sleep(0.1)        
        
def resetPosition():        
    lookStraight()
    
#=========================== camera control back commands ===================
#Vertical movements
def scanUpDown(targetPosition):
    if (targetPosition > vert_up_max) & (targetPosition < vert_down_max):
        pwm.set_pwm(1, 0, targetPosition)
        
#Horizontal movements
def scanLeftRight(targetPosition):
    if (targetPosition >= hori_right_max) & (targetPosition <= hori_left_max):
        pwm.set_pwm(3, 0, targetPosition)        

#========================================================            
setFreq()    
# lookUp90()
# scanRight()
# scanLeft()
# scanDown()
lookStraight()
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
# lookBackRight()
# lookDownMax()
# lookLeft()
# lookRight()
# scanLeft()
# scanRight()
# scanDown()
# lookStraight()
