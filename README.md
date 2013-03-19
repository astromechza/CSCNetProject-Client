CSCNetProject - Client
======================
Client for Participatory Cloud Computing

Random ideas:
-------------
* Talk to other groups about how to develop Server... (or rather WHO will do it)

* At the moment SensorClient.java is the main class. Guessing that in future it could be run like:
    ```
    $ java SensorClient						( spawn a client to send stuff to the server on an auto port )
    $ java SensorClient --serverport 54321	( a specific server port )
    $ java SensorClient --comport 1			( a specific serial port )
    ```
    Or we can use a config file, which could give us a lot more flexibility around the Sensor type, name,
    location or schema.
  
* Hopefully if we design this properly we can run multiple sensor clients at once without interfering.

* Who feels like going absolutely overboard.