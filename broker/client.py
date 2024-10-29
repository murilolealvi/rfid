import paho.mqtt.client as mqtt

from database.mongo import MongodbConnectionHandler
from services.authenticate import AuthenticationHandler
from services.log import LogHandler
from models.log import Log

mongo_conn = MongodbConnectionHandler(db="rfid").connect()
authentication = AuthenticationHandler(mongo_conn, 'tag')
logging = LogHandler(mongo_conn, "log")

class MqttClient:
    def __init__(self, broker_ip, port, client_name, keepalive):
        self.__broker_ip = broker_ip
        self.__port = port
        self.__client_name = client_name
        self.__keepalive = keepalive
        self.start()

    def start(self):
        mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, self.__client_name)
        mqtt_client.connect(host=self.__broker_ip, port=self.__port, keepalive=self.__keepalive)
        mqtt_client.on_message = self.message
        mqtt_client.loop_start()
        self.__client = mqtt_client

    def pub(self, topic, payload):
        self.__client.publish(topic, payload)
    
    def sub(self, topic):
        self.__client.subscribe(topic)

    def message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        user = authentication.authenticate(payload, "id")
        topic = "rfid/authentication"
        if user:
            self.__client.publish(topic, user["name"].encode("utf-8"))
            logging.log(Log(user["name"]))
        else:
            self.__client.publish(topic, str())
        print(msg.topic+": "+ payload)
        print("User: ", user)



