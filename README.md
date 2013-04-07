CSCNetProject - Client
======================
Client for Participatory Cloud Computing

Structure
------------

Client provides the methods required by a client, including interfacing with
Punix.py to capture and record sensor data in a reasonable way.  

A text interface for Client is provided in ClientDriver which uses Menu to
provide a text interface to operate the functions of Client


Testing
------------

I'm including (non-comprehensive) unit testing classes just to make it easy to
check for compatability on senior lab computers and to make sure I'm not going
insane. At the moment, we have:

TestClient.py: Tests, strangely, Client.py

Libraries
-------------
Libraries aren't included. There's a list in library\_downloads.md and a script to automatically set up libraries in library\_setup.sh.

Ideas for future
------------------
* Implement a Heurestic way to create realistic data using a caternary
* Allow Client to be communicated with via command line arguments
