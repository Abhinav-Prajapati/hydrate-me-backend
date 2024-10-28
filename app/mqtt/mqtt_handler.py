# mqtthandler.py

import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.mqtt.config import MQTT_BROKER_URL, MQTT_BROKER_PORT

# MQTT client instance
mqtt_client = mqtt.Client()

def __write_to_db(device_id: str, weight: float, db: Session):
    """
    Function to write the received MQTT data to the database.
    """
    from app.database.models import SensorData
    sensor_data = SensorData(sensor_id=device_id, data=weight)
    db.add(sensor_data)
    db.commit()

def __on_message(client, userdata, msg):
    """
    Callback function to handle incoming MQTT messages.
    """
    message = msg.payload.decode()
    try:
        device_id, data_type, value = message.split("|")
        if data_type == "weight":
            weight = float(value)
            print(f"Received weight `{weight}` for device `{device_id}` on topic `{msg.topic}`")

            # Write to the database using a session from get_db
            with get_db() as session:
                __write_to_db(device_id, weight, session)
            print(f"Data written to database for device `{device_id}`")
        else:
            print(f"Unknown data type `{data_type}`")
    
    except ValueError as ve:
        print(f"ValueError while processing message: {ve}")
    except Exception as e:
        print(f"Error processing message `{message}`: {e}")

def run_mqtt_client():
    """
    Function to initialize the MQTT client, connect to the broker, and subscribe to topics.
    """
    broker = MQTT_BROKER_URL
    port = MQTT_BROKER_PORT
    topic_subscribe = "/weight_change"

    # Set up the callback for receiving messages
    mqtt_client.on_message = __on_message

    # Connect to the broker
    mqtt_client.connect(broker, port)

    # Subscribe to the topic
    mqtt_client.subscribe(topic_subscribe, qos=1)

    # Start the MQTT client loop in a separate thread
    mqtt_client.loop_start()

# Function to publish messages to an MQTT topic
def publish_message(topic: str, message: str):
    mqtt_client.publish(topic, message)
