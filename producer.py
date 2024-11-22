import os
import random
import time
import json
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
load_dotenv()
# Load environment variables
MQTT_BROKER = os.getenv('MQTT_BROKER') 
MQTT_PORT = int(os.getenv('MQTT_PORT'))  
MQTT_TOPIC = os.getenv('MQTT_TOPIC') 
MQTT_USERNAME = os.getenv('MQTT_USERNAME')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
PRODUCER_CLIENT_ID = os.getenv('PRODUCER_CLIENT_ID') 
 
count=0
# Generate random messages
def generate_random_message():
    global count
    count+=1
    message = {
        "temperature": round(random.uniform(20.0, 30.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "status": random.choice(["OK", "ALERT", "CRITICAL"]),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": count
    }
    return json.dumps(message)
 
# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected successfully to MQTT broker with client_id:{PRODUCER_CLIENT_ID}")
    else:
        print(f"Failed to connect, return code {rc}")
 
# MQTT on_publish callback
def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")
 
# MQTT client setup with cleansession set to False and a client ID
client = mqtt.Client(client_id=PRODUCER_CLIENT_ID, clean_session=False)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

 
# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()
 
# Publish messages infinitely
try:
    print("Starting infinite message publishing with cleansession off...")
    while True:
        message = generate_random_message()
        result = client.publish(MQTT_TOPIC, message,qos=1)
       
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Published message: {message}")
        else:
            print(f"Failed to publish message : {result.rc}")
 
        time.sleep(2)  # Wait for 5 seconds before publishing next message
 
except KeyboardInterrupt:
    print("Publishing stopped by user.")
finally:
    client.loop_stop()
    client.disconnect()