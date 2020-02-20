#
# a quick test for speech to text
#
import speech_recognition as sr
import os,sys,signal
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import subprocess
from threading import Thread
import RPi.GPIO as GPIO
import time

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

#sc1 = mqtt.Client(client_id='speechclient1')
#sc1.connect(MQTT_SERVER, 1883, 60)

redport = 15
subprocessPid = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(redport, GPIO.OUT)

     
def set_on():
    GPIO.output(redport,GPIO.HIGH)

def set_off():
    GPIO.output(redport,GPIO.LOW)

def turnOn():
    set_off()
    set_on()

def turnOff():
    set_off()


def main():
    r = sr.Recognizer()
    r.energy_threshold = 400
    with sr.Microphone() as source:
        #r.adjust_for_ambient_noise(source, duration=0.1)  
        #r.dynamic_energy_threshold = True
        print ('say something')
        turnOn()
        audio = r.listen(source)
        print ('done')
        turnOff()
    try:
        text = r.recognize_google(audio)
        text=text.lower()
        print('Neo said:\n' + text)
        #publish.single(MQTT_PATH, 'speech:' + str(text), hostname=MQTT_SERVER)
        if (text.find("right") != -1):
            print('right found')
            publish.single(MQTT_PATH, 'speech:right', hostname=MQTT_SERVER)
            subpid = play_mp3('/home/pi/projects/NewRover/voices/Smitha.mp3')
        if (text.find("left") != -1):
            print('left found')
            subpid = publish.single(MQTT_PATH, 'speech:left', hostname=MQTT_SERVER)
        if (text.find("forward") != -1):
            print('forward found')
            subpid = publish.single(MQTT_PATH, 'speech:forward', hostname=MQTT_SERVER)
            play_mp3('/home/pi/projects/NewRover/voices/Rohan.mp3')
        if (text.find("back") != -1):
            print('backward found')
            subpid = publish.single(MQTT_PATH, 'speech:backward', hostname=MQTT_SERVER)
        if (text.find("stop") != -1):
            print('stop found')
            publish.single(MQTT_PATH, 'speech:stop', hostname=MQTT_SERVER)
            #kill thread ifcommand is to stop
            #if(subprocessPid > 0):
            #    os.killpg(os.getpgid(subprocessPid), signal.SIGTERM)
            #subpid = play_mp3('/home/pi/projects/NewRover/voices/havish.mp3')
            print(subpid)
        if (text.find("up") != -1):
            print('look up')
            subpid = publish.single(MQTT_PATH, 'speech:up', hostname=MQTT_SERVER)
        if (text.find("down") != -1):
            print('look down')
            subpid = publish.single(MQTT_PATH, 'speech:down', hostname=MQTT_SERVER)
        if (text.find("straight") != -1):
            print('look straight')
            subpid = publish.single(MQTT_PATH, 'speech:straight', hostname=MQTT_SERVER)
        if (text.find("roar") != -1) | (text.find("katy") != -1):
            print('Singing katy perry Roar song')
            subpid = play_mp3('/home/pi/Songs/Roar.mp3')
            print(subpid)
            #publish.single(MQTT_PATH, 'speech:song' + subpid, hostname=MQTT_SERVER)
        if (text.find("kotha") != -1) | (text.find("kata")  != -1) | (text.find("pata")  != -1):
            print('Singing Nirmala convent Kotha Kotha basha song')
            subpid = play_mp3('/home/pi/Songs/KothaKotha.mp3')
            #publish.single(MQTT_PATH, 'speech:song' + subpid, hostname=MQTT_SERVER)
        if (text.find("dark horse") != -1):
            print('Singing katy perry Dark Horse song')
            subpid = play_mp3('/home/pi/Songs/DarkHorse.mp3')
            #publish.single(MQTT_PATH, 'speech:song' + subpid, hostname=MQTT_SERVER)
        else: 
            #This steps will find all mp3 files in resource folder to match with search string and then play.
            dir_path = os.path.dirname(os.path.realpath(__file__)) 
            fName=getFile(text)
            #print(str(fName) )
            subpid=play_mp3(str(fName) )
            
    except Exception as e:
        print (e)
    except r.UnKnownValueError:
        print ('error')
    except r.RequestError as e:
        print ('failed'.format(e))
        
def getFile(fileName):
    import glob
    fileName='*' + fileName + '*.mp3'
    results=glob.glob("/home/pi/projects/NewRover/snowboy/resources/" + fileName)
    return results[0]
    
def play_mp3(path):
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    #pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
    #                       shell=True, preexec_fn=os.setsid) 
    subprocess.Popen(['mpg123', '-q', path])
    
    

if __name__ == "__main__":

    x = Thread(target=main(), args=(1,))
    x.start()
        
