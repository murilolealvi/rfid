from broker.client import *
from broker.config import mqtt_broker_config
import time 

mqtt_client = MqttClient(
    mqtt_broker_config["HOST"],
    mqtt_broker_config["PORT"],
    mqtt_broker_config["CLIENT_NAME"],
    mqtt_broker_config["KEEPALIVE"]
)

mqtt_client.sub("rfid/authenticate")

while True: 
    time.sleep(0.01)