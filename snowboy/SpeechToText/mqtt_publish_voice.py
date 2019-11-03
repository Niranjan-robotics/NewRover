import snowboydecoder 
import sys
import signal
import glob
import ntpath
import paho.mqtt.publish as publish

# Demo code for listening two hotwords at the same time

interrupted = False


MQTT_SERVER = "localhost"
MQTT_PATH = "voice"

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

filePaths=[path_leaf(path) for path in all_paths]
print("Order of keywords")
callb=[]
i=0
for f in filePaths:
    i=i+1
    y=str(f).replace("pdml","")
    print(str(i) + "---->" + y)
    #--------- new addition ---------
    callb.append(lambda:snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING))


models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.4]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: publish.single(MQTT_PATH, "robot", hostname=MQTT_SERVER),
             lambda: publish.single(MQTT_PATH, "coco cup", hostname=MQTT_SERVER),
             lambda: publish.single(MQTT_PATH, "coco banana", hostname=MQTT_SERVER),
             lambda: publish.single(MQTT_PATH, "coco face", hostname=MQTT_SERVER)]
print('Listening... Press Ctrl+C to exit')

# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

