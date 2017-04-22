#!python
from iotcommute import WebSocket
import random
import time
# Initialise.
iws = WebSocket("26CGWO23L3WRWUVRJ04N", "BMUMWAS8NEAILTG","client")
# Callback for tick reception.
global value
value=1

def on_tick(tick, ws):
    if "value" in tick:
        print tick["value"]
        value = raw_input("Please enter delay value for LED ")
        ws.send_message("LED",value)

def on_connect(ws):
    print("connection is established")
    ws.get_state("LED")

    
iws.on_tick = on_tick
iws.on_connect = on_connect
# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage
# subscriptions.
iws.connect()
