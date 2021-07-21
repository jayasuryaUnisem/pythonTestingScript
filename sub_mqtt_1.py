# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):  
    client.subscribe("button")  

def on_message(client, userdata, message):
    tempPayload = str(message.payload.decode("utf-8"))
    print("Payload: ", tempPayload)

client = mqtt.Client()  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect('192.168.1.15')
client.loop_start()  # Start networking daemon

while 1:
    print("OK")
    time.sleep(2)
