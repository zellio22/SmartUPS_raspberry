import serial
import paho.mqtt.client as mqtt
import json
import time

# Paramètres du port série
port = '/dev/ttyS0'  # Port série à utiliser
baudrate = 9600  # Débit en bauds

# Paramètres MQTT
broker_address = '192.168.1.14'  # Adresse IP ou nom d'hôte du broker MQTT
port_mqtt = 8500  # Port du broker MQTT
topic = 'smartups'  # Sujet MQTT pour l'envoi des données

# Fonction de callback lors de la connexion MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connecté au broker MQTT')
    else:
        print('Échec de la connexion au broker MQTT')

# Fonction de callback lors de la publication MQTT
def on_publish(client, userdata, mid):
    print('Données publiées avec succès')

# Configuration du client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

# Connexion au broker MQTT
client.connect(broker_address, port=port_mqtt)

# Ouverture du port série
ser = serial.Serial(port, baudrate)

# Lecture et envoi des données en boucle
while True:
    # Lecture de la ligne du port série
    ser.reset_input_buffer()
    time.sleep(1)
    line = ser.readline().decode().strip()
    
#$ SmartUPS V3.2P,Vin GOOD,BATCAP 83,Vout 5250 $

    # Analyse des données
    data = line.split(',')
    if len(data) == 4 and data[0] == '$ SmartUPS V3.2P' and data[1].startswith('Vin') and data[2].startswith('BATCAP') and data[3].startswith('Vout'):
        vin = data[1].split(' ')[1]
        batcap = data[2].split(' ')[1]
        vout = data[3].split(' ')[1]
        
        # Création du message JSON
        message = {
            'Vin': vin,
            'BATCAP': batcap,
            'Vout': vout
        }
        
        # Envoi du message JSON au broker MQTT
        client.publish(topic, json.dumps(message))
        print('Données envoyées :', message)
    
    # Attente de 1 minute
    time.sleep(59)
