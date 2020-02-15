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
    
# tild commands    
        
def lookUp():
    print("Looking up")
    pwm.set_pwm(0, 0, servo_max)
    #publish.single(MQTT_PATH, 'current status: up', hostname=MQTT_SERVER)
    time.sleep(1)
    
def lookStraight():
    print("look straight")
    pwm.set_pwm(0, 0, servo_mid)
    #publish.single(MQTT_PATH, 'current status: straight', hostname=MQTT_SERVER)
    time.sleep(1)
    
def lookDown():
    print("look down")
    pwm.set_pwm(0, 0, servo_min)
    #publish.single(MQTT_PATH, 'current status: down', hostname=MQTT_SERVER)
    time.sleep(1)
    
#setFreq()    
#lookDown()    
#lookStraight()
#lookUp()

