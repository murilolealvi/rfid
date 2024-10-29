# This file is executed on every boot (including wake-boot from deepsleep)

import esp
import os, machine
from umqtt.simple import MQTTClient
import network
import time
import ntptime

import gc

esp.osdebug(None)
gc.collect()

ssid = ""
password = ""
mqtt_server = ""

topic_sub = "rfid/authentication"
topic_pub = "rfid/authenticate"
client_name = "reader"

station = network.WLAN(network.STA_IF)
station.disconnect()
if not station.isconnected():
    print("Connecting to network...")
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
print("Network: : ", station.ifconfig())

try:
    ntptime.settime()
except OSError as e:
    time.sleep(2)
    ntptime.settime()


