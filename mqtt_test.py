import time
import paho.mqtt.client as paho
broker = "192.168.1.15"

def on_message(client, userdata, message):
    time.sleep(1)
    print("Payload: ", str(message.payload.decode("utf-8")))

client = paho.Client("client-001")
client.on_message = on_message

print("Connecting to Broker ", broker)

client.connect(broker)
client.loop_start()
client.publish("test","check1")
client.subscribe("button")
time.sleep(4)
i = 0
while 1:
    i = i+1
    client.publish("test",str(i))
    client.subscribe("button")
    time.sleep(4)
client.disconnect()
client.loop_stop()