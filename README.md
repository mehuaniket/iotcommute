# IOT commute client for Python
--------------------------------
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
```
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
                                          
```
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
```
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
```
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
