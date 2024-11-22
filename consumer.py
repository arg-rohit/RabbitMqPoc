import paho.mqtt.client as mqtt
import os
import time
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
MQTT_BROKER = os.getenv('MQTT_BROKER')  # Default to localhost
MQTT_PORT = int(os.getenv('MQTT_PORT'))  # Default to port 1883
MQTT_TOPIC = os.getenv('MQTT_TOPIC')  # Default topic
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
CONSUMER_CLIENT_ID = os.getenv('CONSUMER_CLIENT_ID')  # Generate a random client ID if none provided

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC, qos=2)

def on_message(client, userdata, msg):
    print(f"Received: {msg.payload.decode()} on topic {msg.topic}")

client = mqtt.Client(client_id=CONSUMER_CLIENT_ID, clean_session=False)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# User-defined intervals
ACTIVE_TIME = 60
DISCONNECT_TIME = 30

while True:
    try:
        # Connect to the broker
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        # Simulate active consumption for user-defined time
        print(f"Consuming messages for {ACTIVE_TIME} seconds...")
        time.sleep(ACTIVE_TIME)

        # Disconnect and simulate a temporary disconnection
        print(f"Disconnecting from MQTT broker for {DISCONNECT_TIME} seconds...")
        client.loop_stop()
        client.disconnect()
        time.sleep(DISCONNECT_TIME)

    except KeyboardInterrupt:
        print("Consumer interrupted by user. Exiting...")
        client.loop_stop()
        client.disconnect()
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)  # Wait before attempting to reconnect
