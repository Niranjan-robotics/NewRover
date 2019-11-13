# Import necessary libraries.
from time import sleep 
import paho.mqtt.publish as publish

MQTT_SERVER = "localhost"
MQTT_PATH = "test_voice"

# Define pin constants

def main():
    sleep(0.3)
    print ("Listening")
    publish.single(MQTT_PATH, 'voice: start recording', hostname=MQTT_SERVER)
    sleep(0.3)
 
 
if __name__ == '__main__':
    main()

     
