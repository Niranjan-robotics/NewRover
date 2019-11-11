# Import necessary libraries.
from time import sleep 
import paho.mqtt.publish as publish
from light import Light

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

# Define pin constants

def main():
    sleep(0.3)
    led = Light(18)
    led.blink
    print ("Listening")
    publish.single(MQTT_PATH, 'voice: start recording', hostname=MQTT_SERVER)
    sleep(3)
 
 
if __name__ == '__main__':
    main()

     
