import pymysql
import matplotlib.pyplot as plt
from io import BytesIO
import time
import paho.mqtt.client as mqtt


# MySQL-Verbindungsinformationen
host = 'localhost'
user = 'root'
password = ''
database = 'werte'
table_temperature = 'temperature_data'
table_humidity = 'humidity_data'

# MQTT Verbindungsdaten
broker_address = "10.68.2.238"
port = 1883
topic_temperature = "sensor/temperature"
topic_humidity = "sensor/humidity"

def create_tables():
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()

        # Tabellen löschen, falls sie existieren
        cursor.execute(f"DROP TABLE IF EXISTS {table_temperature}")
        cursor.execute(f"DROP TABLE IF EXISTS {table_humidity}")

        # Neue Tabellen erstellen für Temperatur und Feuchtigkeit
        cursor.execute(f"CREATE TABLE {table_temperature} (id INT AUTO_INCREMENT PRIMARY KEY, value FLOAT)")
        cursor.execute(f"CREATE TABLE {table_humidity} (id INT AUTO_INCREMENT PRIMARY KEY, value FLOAT)")

        connection.commit()
        print("Neue Tabellen für Temperatur und Feuchtigkeit erstellt")

        cursor.close()
        connection.close()
    except pymysql.Error as e:
        print(f"Fehler beim Erstellen der neuen Tabellen: {e}")

def create_graph(values_temperature, values_humidity):
    try:
        fig, ax = plt.subplots(figsize=(5.4, 4.8))  # Größe auf 800x480 einstellen
        ax.plot(range(len(values_temperature)), values_temperature, color='black', label='Temperature', linewidth=2)
        ax.plot(range(len(values_humidity)), values_humidity, color='black', label='Humidity', linewidth=2)
        ax.set_xlabel('Zeit', fontsize=14, fontweight='bold')  # Schriftgröße und -stärke für die Beschriftungen ändern
        ax.set_ylabel('Werte', fontsize=14, fontweight='bold')
        ax.set_title('Graph der letzten Werte', fontsize=16, fontweight='bold')  # Schriftgröße und -stärke für den Titel ändern
        ax.tick_params(axis='both', which='major', labelsize=14, width=2)  # Dicke der Achsenlinien und Schriftgröße der Achsenbeschriftungen ändern
        for spine in ax.spines.values():  # Ändere die Dicke der Rahmenlinien
            spine.set_linewidth(2)

        ax.legend(prop={'size': 14, 'weight': 'bold'})  # Schriftgröße und -stärke der Legende ändern

        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        with open('graph.png', 'wb') as file:
            file.write(image_stream.read())

        plt.close()  # Schließe das Diagrammfenster

    except Exception as e:
        print(f"Fehler beim Erstellen des Graphen: {e}")


    except Exception as e:
        print(f"Fehler beim Erstellen des Graphen: {e}")

def on_message(client, userdata, message):
    try:
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()

        value = float(message.payload.decode())
        if message.topic == topic_temperature:
            cursor.execute(f"INSERT INTO {table_temperature} (value) VALUES ({value})")
        elif message.topic == topic_humidity:
            cursor.execute(f"INSERT INTO {table_humidity} (value) VALUES ({value})")
        
        connection.commit()
        print(f"Eingefügte Werte in die Datenbank: {value}")

        cursor.execute(f"SELECT value FROM {table_temperature} ORDER BY id DESC LIMIT 30")
        result_temperature = cursor.fetchall()
        values_temperature = [row[0] for row in result_temperature]

        cursor.execute(f"SELECT value FROM {table_humidity} ORDER BY id DESC LIMIT 30")
        result_humidity = cursor.fetchall()
        values_humidity = [row[0] for row in result_humidity]

        cursor.close()
        connection.close()

        create_graph(values_temperature, values_humidity)

    except pymysql.Error as e:
        print(f"Fehler beim Einfügen in die Datenbank: {e}")
        create_graph([], [])  # Zeichne einen leeren Graphen bei Fehlern

def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem MQTT-Broker.")
    client.subscribe(topic_temperature)
    client.subscribe(topic_humidity)

# MQTT-Client initialisieren
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)

create_tables()  # Tabellen erstellen

client.loop_start()  # Starte die Schleife für den MQTT-Client

try:
    while True:
        time.sleep(5)  # Wartezeit für den Empfang neuer Nachrichten
except KeyboardInterrupt:
    print("Programm wird beendet.")
    client.loop_stop()  # Stoppe die Schleife für den MQTT-Client
