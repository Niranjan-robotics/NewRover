import cv2
import numpy as np
import servo
import time

# from PCA9685 import PCA9685

# pwm = PCA9685(0x40, debug=False)
# pwm.setPWMFreq(50)
# pwm.setServoPosition(0, 90)

cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 320)


cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
# cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('Y','U','Y','V'))

_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)

c= str.format("center:{0}   x_medium: {1}",str(center),str(x_medium))
print(c)

#left x_medium = 0 and rightmost = 500 center 250
# To match servo center420 with x-medium center 250 - get diff=420-250 = 170
#To move to left get (x-medium + 170)
position = 410 # center position

#turn left right values
hori_left_max= 520   #left
hori_straight= 420  #Center
hori_right_max= 100   #right

#turn left right values
vert_up_max= 200 ##pwm.set_pwm(0, 100, 200)
vert_straight_= 420  #pwm.set_pwm(0, 0, 420)
vert_down_max= 435  #pwm.set_pwm(0, 50, 450)

servo.lookStraight()

#recenter
def receterPosition():
    x_medium = int(cols / 2)
    center = int(cols / 2)        
    servo.pwm.set_pwm(1, 0, position)
        
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    # _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # check OpenCV version
    major = cv2.__version__.split('.')[0]
    if major == '3':
        ret, contours, hierarchy = cv2.findContours(im.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
        
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w) / 2)
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break
    
    # Move servo motor
    if (position < servo.hori_right_max) or (position > servo.hori_left_max): 
        position = servo.hori_straight_
    elif x_medium < center -30:
        position += (2)
        c= str.format("center:{0}   x_medium: {1}  Position: {2}",str(center),str(x_medium) ,str(position))
        print(c)
    elif x_medium > center + 30:
        position -= (2)
        c= str.format("center:{0}   x_medium: {1}  Position: {2}",str(center),str(x_medium) ,str(position))
        print(c)
        
        
    # servo.pwm.set_pwm(1, 0, position)
    servo.scanLeftRight(position)
    
cap.release()
cv2.destroyAllWindows()

