#
# a quick test for speech to text
#
import speech_recognition as sr
import os,sys,signal
import paho.mqtt.publish as publish
from threading import Thread
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

redport = 15
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
    
    with sr.Microphone() as source:
        print ('say something')
        turnOn()
        audio = r.listen(source)
        print ('done')
        turnOff()
    try:
        text = r.recognize_google(audio)
        print('Neo said:\n' + text)
        
        if 'right' in text:
            print('right found')
            publish.single(MQTT_PATH, 'speech:right', hostname=MQTT_SERVER)
        if 'left' in text:
            print('left found')
            publish.single(MQTT_PATH, 'speech:left', hostname=MQTT_SERVER)
        if 'forward' in text:
            print('forward found')
            publish.single(MQTT_PATH, 'speech:forward', hostname=MQTT_SERVER)
        if 'backward' in text:
            print('backward found')
            publish.single(MQTT_PATH, 'speech:backward', hostname=MQTT_SERVER)
        if 'stop' in text:
            print('stop found')
            publish.single(MQTT_PATH, 'speech:stop', hostname=MQTT_SERVER)
    except Exception as e:
        print (e)
    except r.UnKnownValueError:
        print ('error')
    except r.RequestError as e:
        print ('failed'.format(e))
        

if __name__ == "__main__":
    main()
        
