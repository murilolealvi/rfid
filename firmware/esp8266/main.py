import reader
import utime
from display import I2cLcd
from machine import SoftI2C, Pin, SoftSPI
from card import SDCard

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(4),scl=Pin(5),freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, (16,2))

green = Pin(16, Pin.OUT)
red = Pin(0, Pin.OUT)
green.off()
red.off()

rdr = reader.RC522(14, 13, 12, 2, 15)

def rgb_reset():
    red.off()
    green.off()
    
def scanning():
    lcd.clear()
    rgb_reset()
    lcd.write("Scanning...")

def now():
    timestamp = utime.localtime()
    date = list(timestamp)[2::-1]
    date = "/".join(str(x) for x in date)
    time = f"{str(timestamp[3]-3)}:{str(timestamp[4])}"
    return date, time
    

def callback(topic, msg):
    message = msg.decode()
    if message:
        date, time = now()
        
        lcd.clear()
        lcd.write(message)
        lcd.write(date+" "+time)
        
        green.on()
        utime.sleep(3)
        scanning()
    else:
        lcd.clear()
        lcd.write("*--*--*--*--*--*")
        lcd.write("  UNAUTHORIZED  ")
        red.on()
        utime.sleep(3)
        scanning()
        
    print(f"{topic.decode()} : {message}")
        
    
def start():
    global client_name, mqtt_server, topic_sub
    client = MQTTClient(client_name, mqtt_server, ssl=False)
    client.set_callback(callback)
    client.connect()
    client.subscribe(topic_sub)
    print("Connected to MQTT Broker")
    return client

mqtt_client = start()
scanning()


while True:
    mqtt_client.check_msg()
    # Request cards
    (stat, tag_type) = rdr.request(rdr.PICC_REQIDL)
    if stat == rdr.OK:
        # Anti-collision
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            # Print the uid of the detected card
            rfid = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            mqtt_client.publish(topic_pub, rfid.encode())
            print("RFID:", rfid)
    
    utime.sleep_ms(200)