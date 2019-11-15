from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import time
import paho.mqtt.client as mqtt
MQTT_SERVER = "localhost"
MQTT_PATH = "test_servo"


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min ,mid and max servo pulse lengths
servo_min = 50  # Min pulse length out of 4096
servo_max = 300  # Max pulse length out of 4096
servo_mid = 200  # Max pulse length out of 4096


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
    
def lookUp():
    print("look tilt up")
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)
    
def lookStraight():
    print("look tilt straight")
    pwm.set_pwm(0, 0, servo_mid)
    time.sleep(1)
    
def lookDown():
    print("look tilt down")
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(1)
    
    
