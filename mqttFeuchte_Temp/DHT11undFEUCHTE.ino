#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>


#define DHTPIN 33
#define moisture_sens 32

#define DHTTYPE DHT11


DHT dht(DHTPIN, DHTTYPE);

const char *ssid = "etelti-iot";
const char *password = "iot4ever";
const char *mqttServer = "10.68.2.238";
const int mqttPort = 1883;
const char *mqttTopicTemperature = "sensor/temperature";
const char *mqttTopicHumidity = "sensor/humidity";
const char *mqttTopicWett = "sensor/wett";

WiFiClient espClient;   // Wlan aufbau 
PubSubClient client(espClient); //MQTT Aufbau


float readsensor();  // Aufrufen des Feuchte sensor
int sens1_value =0;
int outputvalue1 = 0;


void setup() {
  Serial.begin(9600);

  // Initialisiere den DHT11-Sensor
  dht.begin();
  
  // Verbinde dich mit dem WLAN
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Verbindung zum WLAN wird hergestellt...");
  }
  Serial.println("Verbunden mit dem WLAN!");

  // Verbinde dich mit dem MQTT-Broker
  client.setServer(mqttServer, mqttPort);

  while (!client.connected()) {
    Serial.println("Verbindung zum MQTT-Broker wird hergestellt...");
    if (client.connect("ESP32Client")) {
      Serial.println("Verbunden mit dem MQTT-Broker!");
    } else {
      Serial.print("Fehler beim Verbinden mit dem MQTT-Broker. Fehlercode: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void loop() {
  // Recupere la temperature et l'humidite du capteur
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  float wett = readsensor();

  // Affiche les valeurs sur le moniteur serie
  //Serial.println("Temperature = " + String(temperature) + " °C");
  //Serial.println("Humidite = " + String(humidity) + " %");

  // Envoie les valeurs via MQTT
  sendMQTTValue(mqttTopicTemperature, temperature);
  sendMQTTValue(mqttTopicHumidity, humidity);
  sendMQTTValue(mqttTopicWett, wett);

  // Attend 10 secondes avant de reboucler
  delay(5000);
}

float readsensor()
{
  sens1_value= analogRead(moisture_sens);
  outputvalue1=map(sens1_value,4095,0,0,100);
  delay(2000);
  return outputvalue1;
}

void sendMQTTValue(const char *topic, float value) {
  // Converti la valeur float en String
  String payload = String(value);

  // Envoie la valeur sur le topic MQTT
  client.publish(topic, payload.c_str());
}

