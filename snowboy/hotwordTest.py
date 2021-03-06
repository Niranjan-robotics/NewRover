import snowboydecoder
import os,sys
import signal
import shlex, subprocess
from subprocess import call
from subprocess import Popen, PIPE
from light import Light

interrupted = False

#mod_path=glob.glob("/home/pi/projects/NewRover/snowboy/trainModels/*_model.pmdl")
    
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python hotwordTest.py ./trainModels/tiger_model.pmdl ")
    sys.exit(-1)

model = sys.argv[1]
print("*******subprocess version********")
print(subprocess.__file__)

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

#ledGreen = Light(18)
def speechtoText():
    #ledGreen.blink()
    bot1 = Popen(["lxterminal", "-e", "python3", "/home/pi/projects/NewRover/publishMsg.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    
detector.start(detected_callback=speechtoText,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
