#!python
from iotcommute import WebSocket
import random
import time
# Initialise.
iws = WebSocket("GK8N7MOTE9XRTVROVRXM", "0OXWDF6GNWS38XV","client")
# Callback for tick reception.
global value
value=1

def on_tick(tick, ws):
    global value
    print tick
    print(tick["value"], tick['sensor'])
    value=value+1
    ws.send_message("LED",value)
    time.sleep(1)
    # Callback for successful connection.

def on_connect(ws):
    print("connection is established")
    ws.get_state("LED")
    ws.send_message("led", random.randint(0, 50))
iws.on_tick = on_tick
iws.on_connect = on_connect
# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage
# subscriptions.
iws.connect()
