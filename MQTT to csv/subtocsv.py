import paho.mqtt.client as mqtt
import csv
import datetime

# Verbindungsinformationen
broker_address = "10.68.2.238"
port = 1883
topic_temperature = "sensor/temperature"
topic_humidity = "sensor/humidity"

# Dateipfad für die Protokolldatei
log_file_path = "sensor_log.csv"

# Callback-Funktion, die aufgerufen wird, wenn eine Nachricht empfangen wird
def on_message(client, userdata, message):
    data = message.payload.decode()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if message.topic == topic_temperature:
        log_data("Temperature", data, timestamp)
    elif message.topic == topic_humidity:
        log_data("Humidity", data, timestamp)

def log_data(sensor_type, value, timestamp):
    with open(log_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, sensor_type, value])
    print(f"{sensor_type} value {value} logged at {timestamp}")

# MQTT-Client initialisieren (ohne explizite Client-ID)
client = mqtt.Client()

# Callback-Funktion dem Client hinzufügen
client.on_message = on_message

# Verbindung zum Broker herstellen
client.connect(broker_address, port)

# Themen abonnieren
client.subscribe(topic_temperature)
client.subscribe(topic_humidity)

# In einer Dauerschleife auf Nachrichten warten
client.loop_forever()
