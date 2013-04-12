CSCNetProject - Client
======================
Client for Participatory Cloud Computing

Structure
------------

Client provides the methods required by a client, including interfacing with
Punix.py to capture and record sensor data in a reasonable way.  

A text interface for Client is provided in ClientDriver which uses Menu to
provide a text interface to operate the functions of Client.

Some very basic and non-comprehensive unit tests are included in TestClient.

How to run
------------

Open ClientDriver.py with python2. 

Files included
------------
    lib/highstocks - a js library from www.highcharts.com/products/highstock to
                     render graphs
    lib/jquery.min.js - a js library required for highstocks to work
    src/ClientDriver.py -  as explained above, a text interface to control the
                           client
    src/Menu.py - as explained above, a module for providing menus
    src/reset_mote - instructions and programs for reseting a mote
    src/templates - html and javascript templates for creating graphs
    src/Client.py
    src/punix.py - modified class from Dominic to record sensor data
    src/serialdump.c and src/serialdump-linux - required by punix to record
                                                data from a sensor.
    src/TestClient.py - as explained above, some unit tests for the client
    src/data - some sample data for testing
