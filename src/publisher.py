from paho.mqtt import client as mqtt_client
import random
import time

broker = 'broker.emqx.io'
port = 1883
topic = '/python/fokson'
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt()

isdo = 'cucc'
while isdo != 3:
    isdo = input('Fonkston 1: goh 2: stahp\n')

    if isdo == '1':
        message = 'goh'
    if isdo == '2':
        message = 'sthap'
    if isdo == '3':
        break
    print(message + '\n')
    result = client.publish(topic, message)