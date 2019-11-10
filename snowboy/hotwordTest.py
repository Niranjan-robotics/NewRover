import snowboydecoder
import os,sys
import signal
from subprocess import call
from subprocess import Popen, PIPE
#from light import Light

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

#led = Light(17)
def speechtoText():
    pid=os.getpid()
    bot1 = Popen(["lxterminal", "-e", "python3", "-i", "/home/pi/projects/NewRover/snowboy/SpeechToText/speech_to_text.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
    os.kill(pid,signal.SIGTERM)

    
detector.start(detected_callback=speechtoText,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
