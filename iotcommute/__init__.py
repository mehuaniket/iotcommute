"""
IOT commute client for Python
-----------------------------
Aniket Patel (c) 2017
License
-------
iot commute Python library is licensed under the MIT License

Design
------
As project statment we are are building library that could work with `IOT 
communicate` project with simplicity.
Basic idea is revolving around Handling client side web-socket connection without
involving user. So he\she could simply intialise connection with just `device-key` 
and `device-id`.After only concern for user is to set funtion on event that callback 
library.
following is basic architecture diagram we're dealing with.

                              |---------|
                              | server  |
                              |---------|
                                  ||
                                  ||
                           |----------------|
                           |tailable cursors|
                           |----------------|
                                  ||
                                  ||
                           |----------------|
                           | websocket      |
                           |----------------|
                                  ||
                                  ||
                           |-----------------|
                           |   iotcommute lib|
                           |-----------------|
                                  ||
                                  ||
                                callbacks
                            |---------------|
                            |client function|
                            |---------------|
                                          

The library
-----------
Iot commute is a set of REST-like APIs  with web socket that expose
many capabilities required to build a application that requires
to pass mesage beetween iot device to client device and client device
t iot device.Execute functions on real time events of iot device
,passing small payloads and data(thorough WebSockets), and more, with the simple web-
socket connection and this all will handle by the iot commute library
This module provides an easy to use abstraction over the direct web-socket connection
with server.
The calls have been converted to methods and their JSON responses
are returned as native Python structures, for example, dicts, lists, bools etc.
See the **[IOT commute documentation](URL)**
for the complete list of events and features, supported parameters and values,
and response formats.
Getting started
---------------
    #!python
    from iotcommute import WebSocket
    # Initialise.
    iws = WebSocket("L1SEIUDU1MC996W48L8Q", "FY6ODPIVU522SY1","device")
    # Callback for tick reception.

    def on_tick(tick, ws):
        print(tick)
        # Callback for successful connection.

    def on_connect(ws):
        print("connection is established")
    iws.on_tick = on_tick
    iws.on_connect = on_connect
    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage
    # subscriptions.
    iws.connect()

A typical web application
-------------------------
In a typical web application where a new instance of
views, controllers etc. are created per incoming HTTP
request, you will need to initialise a new instance of
IOTcommunicate client per request as well. This is because each
individual instance represents a single device that's
authenticated, unlike an **admin** API where you may
use one instance to manage many users.
Hence, in this client application, typically:
- You will initialise an instance of the IotCommute client
- NOTICE:Redirect the user to the `login_url()`
   also for now you directly initialize websocket with genrated keys
-  At the redirect url endpoint, obtain the
`request_token` from the query parameters
-  for now you just pass the tokens and create connection,
   start to communicate.

Exceptions
----------
IotCommute client saves you the hassle of detecting API errors
by looking at codes or JSON error responses. Instead,
it raises aptly named **[exceptions]** that you can catch.
"""

from six import StringIO
import ssl
import csv
import json
import struct
import hashlib
import requests
import threading
import logging

import websocket

import iotcommute.exceptions as ex

# Initialize logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class WebSocket(object):
    """
    The WebSocket client for connecting to Iot Commute streaming messages from service.
    """

    READ_TIMEOUT = 5
    RECONNECT_INTERVAL = 5
    RECONNECT_TRIES = 300

    # Default root API endpoint. It's possible to
    # override this by passing the `root` parameter during initialisation.
    _root = "ws://127.0.0.1/ws"

    def __init__(self, device_id, device_key, side, root=None):
        """
        Initialise websocket client instance.
                - `device_id` is the id issed to you.
        - `device_key` is the API key issued to you.
        - 'user_id' is the NOTICE:it'll included later on.
        - `root` is the websocket API end point root. Unless you explicitly
                want to send API requests to a non-default endpoint, this
                can be ignored.
        """
        self.socket_url = "{root}"\
            "?device={device_id}&key={device_key}&side={side}".format(
                root=root if root else self._root,
                device_id=device_id,
                device_key=device_key,
                side=side
            )
        self.socket = self._create_connection()

        # Placeholders for callbacks.
        self.on_tick = None
        self.on_message = None
        self.on_close = None
        self.on_error = None
        self.on_connect = None
        self.on_reconnect = None
        self.subscribed_tokens = set()
        self.modes = set()

    def _create_connection(self):
        """Create a WebSocket client connection."""
        return websocket.WebSocketApp(self.socket_url,
                                      on_open=self._on_connect,
                                      on_message=self._on_message,
                                      on_data=self._on_data,
                                      on_error=self._on_error,
                                      on_close=self._on_close)

    def connect(self, threaded=False, disable_ssl_verification=False, proxy=None):
        """
        Start a WebSocket connection as a seperate thread.
        - `threaded` when set to True will open the connection
                in a new thread without blocking the main thread
        - `disable_ssl_verification` when set to True will disable ssl cert verifcation. Default is False.
        - `proxy` (dict) to set http proxy. Default is None.
                List of config
                        `host` - http proxy host name.
                        `port` - http proxy port. If not set, set to 80.
                        `auth` - http proxy auth information (tuple of username and password. default is None)
                Example:
                        ```
                        proxy = {
                                'host': 'testhost',
                                'port': 3000,
                                'auth': ('username', 'password')
                        }
                        ```
        """
        kwargs = {}

        if proxy and proxy.get("host"):
            kwargs["http_proxy_host"] = proxy.get("host")
            kwargs["http_proxy_port"] = proxy.get("port")
            kwargs["http_proxy_auth"] = proxy.get("auth")

        if disable_ssl_verification:
            kwargs["sslopt"] = {"cert_reqs": ssl.CERT_NONE}

        if not threaded:
            self.socket.run_forever(**kwargs)
        else:
            self.websocket_thread = threading.Thread(
                target=self.socket.run_forever, kwargs=kwargs)
            self.websocket_thread.daemon = True
            self.websocket_thread.start()

        return self

    def is_connected(self):
        """Check if WebSocket connection is established."""
        if self.socket and self.socket.sock:
            return self.socket.sock.connected
        else:
            return False

    def reconnect(self):
        """Reconnect WebSocket connection if it is not connected."""
        if not self.is_connected():
            self.socket = self._create_connection()

        return True

    def close(self):
        """Close the WebSocket connection."""
        self.socket.close()

    def _on_connect(self, ws):
        if self.on_connect:
            self.on_connect(self)

    def _on_data(self, ws, data, resp_type, data_continue):
        """Receive raw data from websocket."""
        if self.on_tick:
            data=json.loads(data)
            self.on_tick(data, self)

    def _on_close(self, ws):
        """Call 'on_close' callback when connection is closed."""
        if self.on_close:
            self.on_close(self)

    def _on_error(self, ws, error):
        """Call 'on_error' callback when connection throws an error."""
        if self.on_error:
            self.on_error(error, self)

        self.socket.close()

    def _on_message(self, ws, message):
        """Call 'on_message' callback when text message is received."""
        if self.on_message:
            self.on_message(message, self)

    def send_message(self, sensor, value):
        """
        this function will help client to send message to server in abstract way 
        only take sensor name or id and value as parameter
        if you want send message as you wish use send_payload() method.
        """
        try:
            struct_msg = {"method": "put", "status": {
                "sensor": sensor, "value": value}}
            self.socket.send(json.dumps(struct_msg))
            return True
        except:
            self.socket.close()
            raise

    def get_state(self, sensor):
        """
        this function will get last state of sensor you just need to pass sensor name.
        next json will be the sensor state.so you need to run this only in starting stage.
        otherwise it hard to keep track of.
        """
        try:
            struct_msg = {"method": "get", "sensor": sensor}
            self.socket.send(json.dumps(struct_msg))
            return True
        except:
            self.socket.close()
            raise
    def send_payload(self,payload):
        """
        this function will help client to send message to server in abstract way 
        only take sensor name or id and value as parameter
        if you want send message as you wish use send_payload() method.
        """
        try:
            struct_msg = {"method": "put", "status": payload}
            self.socket.send(json.dumps(struct_msg))
            return True
        except:
            self.socket.close()
            raise
