#!python
from iotcommute import WebSocket
import random
import time
import serial
# Initialise.
iws = WebSocket("26CGWO23L3WRWUVRJ04N", "BMUMWAS8NEAILTG","device")
try:
    ser = serial.Serial('/dev/cu.usbmodemFA131',9600)
except serial.serialutil.SerialException:
    print "Connect your arduino device correctly"

# Callback for tick reception.

def on_tick(tick, ws):
    global ser  
    ser.write(str(tick['value']))
    print tick['value']
    # Callback for successful connection.

def on_connect(ws):
    print("connection is established")
    ws.get_state("LED")
iws.on_tick = on_tick
iws.on_connect = on_connect
# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage
# subscriptions.
iws.connect()
