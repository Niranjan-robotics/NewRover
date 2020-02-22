#!/usr/bin/python3

#
# ****************************************************************************
# Detect and annotate objects on a LIVE camera feed
# using the Google Coral USB Stick.
#
# Works with both Raspberry Pi Camera and USB Camera
# (see ARGS for how to switch bewtween these).
#
# Version 2: Fixed percentage display and assume that all files are under the
# same directory.
#
# ****************************************************************************
#
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import cv2
import sys
import numpy
import ntpath
import argparse
import time
from time import sleep
from threading import Thread
from PIL import Image
import PIL.ImageDraw
import PIL.ImageFont
import edgetpu.detection.engine
from edgetpu.utils import image_processing
from edgetpu.detection.engine import DetectionEngine
from edgetpu.basic import edgetpu_utils
from imutils.video import FPS
from imutils.video import VideoStream
import multiprocessing as mp

MQTT_SERVER = "localhost"
MQTT_PATH = "test_objectdetection"

message = "face"
action = False
processes = []
# Variable to store command line arguments
ARGS = None

    
# Read labels from text files.
def ReadLabelFile(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret

# Annotate and display video
def annotate_and_display ( image, inferenceResults, elapsedMs, labels, font ):

    # Iterate through result list. Note that results are already sorted by
    # confidence score (highest to lowest) and records with a lower score
    # than the threshold are already removed.
    result_size = len(inferenceResults)
    for idx, obj in enumerate(inferenceResults):

        # Prepare image for drawing
        draw = PIL.ImageDraw.Draw( image )

        # Prepare boundary box
        box = obj.bounding_box.flatten().tolist()
                
        # Draw rectangle to desired thickness
        for x in range( 0, 4 ):
            draw.rectangle(box, outline=(255, 255, 0) )

        # Annotate image with label and confidence score
        display_str = labels[obj.label_id] + ": " + str(round(obj.score*100, 2)) + "%"
        draw.text( (box[0], box[1]), display_str, font=font )

        box = obj.bounding_box.flatten().astype("int")
        (startX, startY, endX, endY) = box
        
        # Log the current result to terminal
        print("Object (" + str(idx+1) + " of " + str(result_size) + "): "
              + labels[obj.label_id] + " (" + str(obj.label_id) + ")"
              + ", Confidence:" + str(obj.score)
              + ", Elapsed:" + str(elapsedMs*1000.0) + "ms"
              + ", Box:" + str(box))
        dataPub = labels[obj.label_id] + " " + "Confidence:" + str(obj.score) + ", Elapsed:" + str(elapsedMs*1000.0) + "ms" + ", Box:" + str(box)
        dataPub = str(endX)
        
        objX = endX-startX
        objX = objX / 2
        objX = objX + startX
        objY = endY-startY
        objY = objY / 2
        objY = objY + startY
        outputString = labels[obj.label_id] + ":" + str(endX-startX)
        outputString = outputString + ";" + str(endY-startY)  # str can only take 3 objects or something like that
        outputString = outputString + "@" + str(objX)
        outputString = outputString + "#" + str(objY)
        
        #client.publish(MQTT_PATH, outputString)
        publish.single(MQTT_PATH, 'objectdetection: ' + outputString, hostname=MQTT_SERVER)

    # If a display is available, show the image on which inference was performed
    if 'DISPLAY' in os.environ:
        displayImage = numpy.asarray( image )
        cv2.imshow( 'NCS Improved live inference', displayImage )

def main():

    # Load the labels file
    labels =[ line.rstrip('\n') for line in
              open( ARGS.labels ) if line != 'classes\n']

    print(ARGS)
    # Load the labels file
    labels =[ line.rstrip('\n') for line in
              open( ARGS.labels ) if line != 'classes\n']

    # Store labels for matching with inference results
    labels = ReadLabelFile(ARGS.labels) if ARGS.labels else None

    # Specify font for labels
    font = PIL.ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf", 20)

    # If --picamera is not set then default to USB Camera
    if ARGS.picamera:
        print("Using Video Stream from PiCamera.")
    else:
        print("Using Video Stream from USB Camera.")

    # Use Google Corals own DetectionEngine for handling
    # communication with the Coral
    inferenceEngine = edgetpu.detection.engine.DetectionEngine('./all_models/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite') #'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    #inferenceEngine = edgetpu.detection.engine.DetectionEngine('mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    # #============= niranjan edited ============
    # camera_device = ARGS.picamera
    # #-- 2. Read the video stream
    vs = cv2.VideoCapture(0)
    # # set the format into MJPG in the FourCC format 
    vs.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    if not vs.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    
    # #============== end edit======= uncomment following commented lines when not using above code====================
    ## Use imutils to count Frames Per Second (FPS)
    fps = FPS().start()

    ## Capture live stream & send frames for preprocessing, inference and annotation
    while message.find('face') != -1:
        try:

            # Read frame from video and prepare for inference
            frame, screenshot = vs.read()

            # Prepare screenshot for annotation by reading it into a PIL IMAGE object
            image = Image.fromarray(screenshot)

            # Perform inference and note time taken
            startMs = time.time()
            inferenceResults = inferenceEngine.DetectWithImage(image, threshold=ARGS.confidence, keep_aspect_ratio=True, relative_coord=False, top_k=ARGS.maxobjects)
            elapsedMs = time.time() - startMs

            # Annotate and display
            annotate_and_display( image, inferenceResults, elapsedMs, labels, font )

            # Display the frame for 5ms, and close the window so that the next
            # frame can be displayed. Close the window if 'q' or 'Q' is pressed.
            if( cv2.waitKey( 2 ) & 0xFF == ord( 'q' ) ):
                fps.stop()
                break

            fps.update()

        # Allows graceful exit using ctrl-c (handy for headless mode).
        except KeyboardInterrupt:
            fps.stop()
            break
    
    vs.release()
    cv2.destroyAllWindows()
    vs.stop()
    time.sleep(2)


if __name__ == "__main__":

    print("I am in object detection")
    t2 = Thread()
    t2.setDaemon(True)
    t2.start()
    
    # comment following line to stop detecting facemessage
    #message='face'
    
    parser = argparse.ArgumentParser(
                         description="Detect objects on a LIVE camera feed using \
                         Google Coral USB." )

    parser.add_argument( '--model', type=str,
                         default='/home/pi/edgetpu/niranjan_trained_model_edgetpu.tflite',
                         #default='./all_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite',
                         help="Path to the neural network graph file." )

    parser.add_argument( '--labels', type=str,
                         default='./all_models/coco_labels.txt',
                         help="Path to labels file." )

    parser.add_argument( '--maxobjects', type=int,
                         default=3,
                         help="Maximum objects to infer in each frame of video." )

    parser.add_argument( '--confidence', type=float,
                         default=0.75, 
                         help="Minimum confidence threshold to tag objects." )

    parser.add_argument( '--picamera',
                         action='store_true',
                         help="Use PiCamera for image capture. If this flag is not set a USB Camera will be expected.")

    parser.set_defaults(picamera=False)

    ARGS = parser.parse_args()
    main()

