from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tilt = 19

# Configure min ,mid and max servo pulse lengths
servo_tilt_up = 70 # upto 130
servo_tilt_straight = 0 #up to 20
servo_tilt_down = -20

GPIO.setup(tilt, GPIO.OUT) # white => TILT

def setServoAngle(servo, angle):
	assert angle >=-20 and angle <= 130
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()  
    
def tiltUp():
    print("look tilt up")
    setServoAngle(tilt,servo_tilt_up)
    
def tiltStraight():
    print("look tilt straight")
    setServoAngle(tilt,servo_tilt_straight)
    
def tiltDown():
    print("look tilt down")
    setServoAngle(tilt,servo_tilt_down)
    

#if __name__ == '__main__':  
#    tiltDown()
#    tiltUp()
#    tiltStraight()
    
#    GPIO.cleanup()
