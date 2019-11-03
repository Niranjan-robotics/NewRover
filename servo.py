from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()

# Configure min ,mid and max servo pulse lengths

servo_pan_straight = 376
servo_pan_right = 170 
servo_pan_left = 600

servo_tilt_up = 300
servo_tilt_straight = 170 
servo_tilt_back = 600
servo_tilt_down = 100


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel,0,pulse)
    
def setSevoAngle(channel, pulse):
    pwm.set_pwm(channel,0,pulse)
    time.sleep(1)
 
def panStraight():
    print("look pan straight")
    setSevoAngle(0,servo_pan_straight)
    time.sleep(0.5)
def panRight():
    print("look pan Right")
    setSevoAngle(0,servo_pan_right)
    time.sleep(0.5)
def panLeft():
    print("look pan Left")
    setSevoAngle(0,servo_pan_left)
    time.sleep(0.5)
    
def tiltUp():
    print("look tilt up")
    setSevoAngle(1,servo_tilt_up)
    time.sleep(0.5)
def tiltStraight():
    print("look tilt straight")
    setSevoAngle(1,servo_tilt_straight)
    time.sleep(0.5)
def tiltBack():
    print("look tilt back")
    setSevoAngle(1,servo_tilt_back)
    time.sleep(0.5)   
def tiltDown():
    print("look tilt down")
    setSevoAngle(1,servo_tilt_down)
    time.sleep(0.5) 
    
def lookStraight():
    tiltStraight()
    panStraight()

# tiltBack()
# tiltUp()
# tiltStraight()
# tiltDown()
#panRight()
#panLeft()
#panStraight()      
