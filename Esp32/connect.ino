#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT22

WiFiClient esp32Client;
PubSubClient mqttClient(esp32Client);
DHT dht(DHTPIN, DHTTYPE);

const char *SSID = "20183748";
const char *PASSWORD = "20183748@@";

const char *MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char *MQTT_TOPIC = "dht";
const char *MQTT_CLIENT_NAME = "ashley";

const int DHT22_DELAY = 3000;
const int RECHECK_INTERVAL = 500;
const int PUBLISH_INTERVAL = 1000;

long lastReconnectAttempt = 0;
long lastPublishAttempt = 0;

void setup()
{
    Serial.begin(115200);
    delay(10);

    setupWifi();
    dht.begin();
    setupMQTT();
}

void loop()
{
    long now = millis();

    if (!mqttClient.connected())
    {
        if (now - lastReconnectAttempt > RECHECK_INTERVAL)
        {
            lastReconnectAttempt = now;
            mqttClient.connect(MQTT_CLIENT_NAME);

            if (mqttClient.connected())
            {
                // Resubscribe to any topics, if necessary
                // This is also a good place to publish an error to a separate topic!
            }
        }
    }
    else
    {
        if (now - lastPublishAttempt > PUBLISH_INTERVAL)
        {
            lastPublishAttempt = now;
            readAndPublishData();
            mqttClient.loop();
        }
    }
}

void setupWifi()
{
    Serial.println("");
    Serial.print("Connecting to ");
    Serial.print(SSID);

    WiFi.begin(SSID, PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(RECHECK_INTERVAL);
        Serial.print(".");
        yield();
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void setupMQTT()
{
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);

    Serial.println("");
    Serial.print("Connecting to MQTT");

    while (!mqttClient.connected())
    {
        Serial.print(".");
        mqttClient.connect(MQTT_CLIENT_NAME);
        delay(RECHECK_INTERVAL);
    }

    Serial.println("");
    Serial.println("Connected!");
    Serial.println("");
}

void readAndPublishData()
{
    if (mqttClient.connected())
    {
        float tempC = dht.readTemperature();
        float humidity = dht.readHumidity();

        StaticJsonDocument<256> doc;

        doc["temp"] = tempC;
        doc["humi"] = humidity;

        char out[128];
        int b = serializeJson(doc, out);
        Serial.println("Sending message to MQTT topic..");
        Serial.println(b);

        if (mqttClient.publish(MQTT_TOPIC, out) == true)
        {
            Serial.println("Success sending message");
        }
        else
        {
            Serial.println("Error sending message");
        }

        mqttClient.loop();
        Serial.println("-------------");
    }
}