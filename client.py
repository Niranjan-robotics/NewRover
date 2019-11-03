import paho.mqtt.client as mqtt
 
MQTT_SERVER = "192.168.1.108"
MQTT_PATH = "test_channel"
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    tf_in=str(msg.payload)
    #print(tf_in)
    #print(tf_in.find("coco distance:"))
    if (tf_in.find("coco distance:") != -1):
        length = len(tf_in)
        pos1 = tf_in.find(':')  # split up the input string
        #print(pos1)
        distanceString = tf_in[(pos1+1):(length)]  # this will give you the width of the person
        distanceString=distanceString.replace("'","")
        distance = int(distanceString)
        #print(distance)
        currentDetection="distance"
        
        if (distance > 10):
            print("Object is little far : " + str(distance))
            client.publish("test_servo", "start")
        if (distance < 10):
            print("Object is little close : " + str(distance))
            client.publish("test_servo", "stop")

    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

