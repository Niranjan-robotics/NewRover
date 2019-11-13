# -*- coding: utf-8 -*-

"""
Subscriber.

Reference:
https://www.ev3dev.org/docs/tutorials/sending-and-receiving-messages-with-mqtt/
"""

import paho.mqtt.client as mqtt


host = 'localhost'


def on_connect(client, userdata, flags, rc):
    """On client connect."""
    print("Connected with result code " + str(rc))
    client.subscribe("/test/hello")
    client.subscribe("/test/world")
    client.subscribe("test_voice")



def on_message(client, userdata, msg):
    """On sending a message."""
    if msg.payload:
        print(str(msg.payload))
    else:
        print("No message was sent!")


if __name__ == '__main__':
    client = mqtt.Client()
    client.connect(host, 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()
