from dotenv import load_dotenv
import os 

load_dotenv(".env")

MQTT_TOPIC = 'sensor/data'

MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL", "localhost")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))

# Second parameter passed to os.getenv() are default values

