import os
import cv2
import time
from subprocess import call
from subprocess import Popen, PIPE
import paho.mqtt.client as mqtt

#usage - use listener of this message =
#    pi@raspberrypi:~/projects/NewRover $ python3 camera_servo_intergration.py

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
if not camera.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
        
return_value, image = camera.read()
i=0

currentDirectory = os.getcwd()

filePath=currentDirectory + '/myClassifyimage.png'

cv2.imwrite(filePath, image)
time.sleep(0.5)
# image = cv2.imread(image_path)
# image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# imH, imW, _ = image.shape 
# image_resized = cv2.resize(image_rgb, (width, height))
# input_data = np.expand_dims(image_resized, axis=0)

del(camera)

#print(filePath)
msgout = Popen(["bash /home/pi/projects/NewRover/ClassifyImageRuntime.sh %s" %(filePath)], shell = True,stdout=PIPE, stderr=PIPE, stdin=PIPE)
