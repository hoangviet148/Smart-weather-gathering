#include <WiFi.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_I2CDevice.h>
#include <Adafruit_BMP085.h>

#define DHTPIN 4
int MLPIN = 15;
int REF = 5;
#define DHTTYPE DHT22

WiFiClient esp32Client;
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085 bmp;

const char *SSID = "Hiu";
const char *PASSWORD = "987654321";

const char *serverName = "http://f56d1807322f.ngrok.io/api/postSensorData";

long lastReconnectAttempt = 0;
long lastPublishAttempt = 0;

unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

void setup()
{
    Serial.begin(115200);
    pinMode(MLPIN, INPUT);
    pinMode(REF, INPUT);
    delay(10);

    setupWifi();
    dht.begin();
    bool a = bmp.begin();
    if (!bmp.begin())
    {
        Serial.println("Could not find a valid BMP085/BMP180 sensor, check wiring!");
        while (1)
        {
        }
    }
}

void loop()
{
    long now = millis();
    if ((now - lastTime) > timerDelay)
    {
        //Check WiFi connection status
        if (WiFi.status() == WL_CONNECTED)
        {
            HTTPClient http;

            http.begin(serverName);

            // Specify content-type header
            http.addHeader("Content-Type", "application/json");
            //http.addHeader("Content-Type", "application/x-www-form-urlencoded");
            int uvLevel = averageAnalogRead(MLPIN);
            int refLevel = averageAnalogRead(REF);
            //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
            float outputVoltage = 1.0 * 3.3 / refLevel * uvLevel;
            float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0); //Convert the voltage to a UV intensity level
            if (isnan(uvLevel))
            {
                Serial.println("Failed to read uv from ml8511 sensor!");
            }

            float pressure = bmp.readPressure();
            if (isnan(pressure))
            {
                Serial.println("Failed to read pressure from bmp sensor!");
            }
            float tempC = dht.readTemperature();
            if (isnan(tempC))
            {
                Serial.println("Failed to read tempC from DHT sensor!");
            }
            float humidity = dht.readHumidity();
            if (isnan(humidity))
            {
                Serial.println("Failed to read humi from DHT sensor!");
            }

            Serial.print(F("Humidity: "));
            Serial.print(humidity);
            Serial.print(F(", Temperature: "));
            Serial.print(tempC);
            Serial.print(F(", Pressure: "));
            Serial.print(pressure);
            Serial.print(F(", UV: "));
            Serial.print(uvLevel);

            //int uvLevel = averageAnalogRead(MLPIN);
            //int refLevel = averageAnalogRead(REF);

            StaticJsonDocument<200> doc;

            doc["temperature"] = tempC;
            doc["humidity"] = humidity;
            doc["uv"] = uvLevel;
            doc["pressure"] = pressure;

            char out[128];
            int b = serializeJson(doc, out);
            Serial.println("\nSending message to HTTP request...");
            //Serial.println(b);

            int httpResponseCode = http.POST(out);
            if (httpResponseCode > 0)
            {
                Serial.print("HTTP Response code: ");
                Serial.println(httpResponseCode);
                String payload = http.getString();
                Serial.println(payload);
            }
            else
            {
                Serial.print("Error code: ");
                Serial.println(httpResponseCode);
            }
            // Free resources
            http.end();
        }
        else
        {
            Serial.println("WiFi Disconnected");
        }
        lastTime = millis();
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
        delay(500);
        Serial.print(".");
        yield();
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

int averageAnalogRead(int pinToRead) {
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 
 
  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;
 
  return(runningValue);
}
 
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
 