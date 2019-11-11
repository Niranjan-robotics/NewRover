#
# a quick test for speech to text
#
import speech_recognition as sr
import os,sys,signal
import paho.mqtt.publish as publish
from threading import Thread
import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    tf_in = (str(msg.payload))
    
    if (tf_in.find("voice:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        #print(pos1)
        speechString = tf_in[(pos1+1):(length)]  # this will give you the width of the person
        speechString=distanceString.replace("'","")
        print(speechString)
        
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)
    
    
def main():

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print ('say something')
        audio = r.listen(source)
        print ('done')
    try:
        text = r.recognize_google(audio)
        print('Neo said:\n' + text)
        publish.single(MQTT_PATH, 'voice:' + text, hostname=MQTT_SERVER)

        if 'right' in text:
            print('right found')
        if 'left' in text:
            print('left found')
        if 'forward' in text:
            print('forward found')
        if 'backward' in text:
            print('backward found')
        if 'stop' in text:
            print('stop found')
    except Exception as e:
        print (e)
    except r.UnKnownValueError:
        print ('error')
    except r.RequestError as e:
        print ('failed'.format(e))


if __name__ == "__main__":
    main()
