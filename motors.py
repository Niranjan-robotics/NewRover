
import RPi.GPIO as GPIO
from time import sleep

'''
m1in1 = 4
m1in2 = 14
m1en = 20
 
m2in1 = 17
m2in2 = 18 / 
m2en = 21
temp1 = 1

'''
m1in1 = 9
m1in2 = 25
m1en = 20
 
m2in1 = 8
m2in2 = 11
m2en = 21
temp1 = 1

GPIO.setmode(GPIO.BCM)

timetoHold = False

def init():
    GPIO.output(m1en,GPIO.HIGH) #ENABLE 1
    GPIO.output(m2en,GPIO.HIGH) #ENABLE 2
    
def pinset():
    GPIO.setup(m1in1,GPIO.OUT)
    GPIO.setup(m1in2,GPIO.OUT)
    GPIO.setup(m2in1,GPIO.OUT)
    GPIO.setup(m2in2,GPIO.OUT)
    GPIO.setup(m1en,GPIO.OUT) 
    GPIO.setup(m2en,GPIO.OUT)

def goForward():
    GPIO.output(m1in1,GPIO.HIGH)
    GPIO.output(m1in2,GPIO.LOW)
    GPIO.output(m2in1,GPIO.HIGH)
    GPIO.output(m2in2,GPIO.LOW)
    
def goBackward():
    GPIO.output(m1in1,GPIO.LOW)
    GPIO.output(m1in2,GPIO.HIGH)
    GPIO.output(m2in1,GPIO.LOW)
    GPIO.output(m2in2,GPIO.HIGH)
    
def turnRight():
    print("Turning Right")
    GPIO.output(m1in1,GPIO.HIGH)
    GPIO.output(m1in2,GPIO.LOW)
    GPIO.output(m2in1,GPIO.LOW)
    GPIO.output(m2in2,GPIO.HIGH)

def turnLeft():
    GPIO.output(m1in1,GPIO.LOW)
    GPIO.output(m1in2,GPIO.HIGH)
    GPIO.output(m2in1,GPIO.HIGH)
    GPIO.output(m2in2,GPIO.LOW)

def stopThere():
    print("Rohan and Havish asked me to stop")
    GPIO.output(m1in1,GPIO.LOW)
    GPIO.output(m1in2,GPIO.LOW)
    GPIO.output(m2in1,GPIO.LOW)
    GPIO.output(m2in2,GPIO.LOW)
    sleep(0.5)

def goToSleep():
    GPIO.cleanup()
    
def motorSetup():
    #initialize     
    pinset()
    init()

def speedUp():
    p1.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)
    
def speedDown():
    print("medium")
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)
    

motorSetup()
p1=GPIO.PWM(m1en,1000)
p2=GPIO.PWM(m2en,1000)


p1.start(100)
p2.start(100)

#initially stops
stopThere()
#=================================
