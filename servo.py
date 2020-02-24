from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
MQTT_SERVER = "localhost"
MQTT_PATH = "test_servo"


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min ,mid and max servo pulse lengths
servo_min = -20  # Min pulse length out of 4096
servo_max = 70  # Max pulse length out of 4096
servo_mid = 0  # Max pulse length out of 4096


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
    pwm.set_pwm(0, 100, 200)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: up', hostname=MQTT_SERVER)
    
def lookUp70():
    print("Looking up")
    #look 90 degree up
    #look straigh and up 70 degree
    pwm.set_pwm(0, 100, 300)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: up', hostname=MQTT_SERVER)
    
def lookStraight():
    print("look straight")
    pwm.set_pwm(0, 100, 300)
    time.sleep(1)
    pwm.set_pwm(1, 0, 420)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)
    
def lookDownMax():
    print("look down")
    pwm.set_pwm(0, 50, 450)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: down', hostname=MQTT_SERVER)
    time.sleep(1)

def lookLeft():
    print("look left")
    pwm.set_pwm(0, 0, 300)
    time.sleep(1)
    pwm.set_pwm(1, 0, 420)
    time.sleep(1)
    pwm.set_pwm(1, 0, 600)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)

def lookRight():
    print("look left")
    pwm.set_pwm(0, 100, 300)
    time.sleep(1)
    pwm.set_pwm(1, 0, 250)
    time.sleep(1)
    pwm.set_pwm(0, 100, 300)
    time.sleep(1)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)

def lookBackRight():
    print("look back")
    pwm.set_pwm(0, 0, 24)
    time.sleep(1)
    pwm.set_pwm(1, 0, 24)
    time.sleep(1)
    pwm.set_pwm(1, 0, 250)
    time.sleep(1)

def MultiAngleTest():
    for i in range(180):
        pwm.set_pwm( i)
    for i in range(180):
        pwm.set_pwm(1, 0,180 - i)
    deInitServo()
    

setFreq()    
lookUp90()
lookStraight()
lookLeft()
lookRight()


# #============================================== look up down ===========
# #look up
# pwm.set_pwm(0, 0, 24)
# pwm.set_pwm(1, 0, 24)
# time.sleep(1)
# #look strait
# pwm.set_pwm(0, 0, 24)

# time.sleep(1)
# #pwm.set_pwm(0, 0, 180)

# time.sleep(1)

# pwm.set_pwm(0, 0, 350)
# # #left
# #pwm.set_pwm(1, 1024, 3072)
# time.sleep(2)
# #straight
# pwm.set_pwm(1, 0, 420)
# time.sleep(2)
# pwm.set_pwm(0, 0, 300)
# time.sleep(2)
# #look straigh and up 70 degree
# pwm.set_pwm(0, 100, 300)
# time.sleep(2)
# #look 90 degree up
# pwm.set_pwm(0, 100, 200)
# time.sleep(2)

# #look down forward -max
# pwm.set_pwm(0, 50, 450)
# time.sleep(1)


# #to move right first reset to straight
# pwm.set_pwm(0, 100, 300)
# time.sleep(1)
# pwm.set_pwm(1, 0, 250)
# time.sleep(1)
# pwm.set_pwm(0, 100, 300)
# time.sleep(1)

# #to move left first reset to straight
# pwm.set_pwm(0, 0, 300)
# time.sleep(1)
# pwm.set_pwm(1, 0, 420)
# time.sleep(1)
# pwm.set_pwm(1, 0, 600)
# time.sleep(1)
