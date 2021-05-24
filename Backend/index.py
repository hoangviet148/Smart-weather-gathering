from flask import Flask, request
import paho.mqtt.client as mqtt
import json
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb+srv://travel:14802000@cluster0.qvr9i.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
myDB = client["weather-gathering"]
myCol = myDB["data"]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("dht1")

# The callback for when a PUBLISH message is received from the ESP32.


def on_message(client, userdata, msg):
    if (msg.topic == "dht1"):
        print("DHT reading update: ")
        print(msg.payload)
        payload = json.loads(msg.payload)
        print(payload['temp'])
        myCol.insert_one(payload)


mqttC = mqtt.Client()
mqttC.on_connect = on_connect
mqttC.on_message = on_message
mqttC.connect("broker.hivemq.com", 1883, 60)
mqttC.loop_start()

if __name__ == "__main__":
    app.run(host="localhost", port=3000)
