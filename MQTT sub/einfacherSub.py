import paho.mqtt.client as mqtt

# Verbindungsinformationen
broker_address = "10.68.2.238"
port = 1883
topic_temperature = "sensor/temperature"
topic_humidity = "sensor/humidity"

# Callback-Funktion, die aufgerufen wird, wenn eine Nachricht empfangen wird
def on_message(client, userdata, message):
    print(f"Empfangene Nachricht auf Thema {message.topic}: {message.payload.decode()}")

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
