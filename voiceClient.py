# Import necessary libraries.
from time import sleep
from threading import Thread 
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from light import Light

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

# Define pin constants
firstRun = True
listening = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    global firstRun
    global listening
    
    tf_in = (str(msg.payload))
    
    if (tf_in.find("voice:") != -1):
        if (tf_in.find("speech:") != -1):
            print("Ready for speech")
            led = Light(15)
            led.blink
            sleep(0.3)
        else:
            length = len(tf_in)
            pos1 = tf_in.find(':')  # split up the input string
            listening = True
            speechString = tf_in[(pos1+1):(length)]  # this will give you the width of the person
            speechString=distanceString.replace("'","")
            print(speechString)
        
client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 60)

def runB():
    #client = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    #client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
 
if __name__ == '__main__':
    t2 = Thread(target = runB)
    t2.setDaemon(True)
    t2.start()
    try:
        while True:
            firstRun == False
            if (listening == True):
                print("I am Listening")
                sleep(0.3)
                led = Light(18)
                led.blink
                listening = False
                publish.single(MQTT_PATH, 'speech: speech to text', hostname=MQTT_SERVER)
                
    # Keep looping until a key is pressed.
    except KeyboardInterrupt:
        GPIO.cleanup()
        client.disconnect()
     
