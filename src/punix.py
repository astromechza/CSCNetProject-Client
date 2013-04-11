#!/usr/bin/python
# -*- coding: ascii -*-

# Simple class to get sensor data captured by serialdump-linux.c (provided by 
#  Adam Dunkels @SICS) from sensor mote.
# Executes serialdump as a sub process and pipes the output here 
# Usage python unix.py /dev/ttyUSB0
# To turn debugging off: python -O <args ...>
# Original Author: Dominic Follett

# Modified by Steven Rybicki, 6 April 2013

import sys, subprocess, shlex, signal
import time
class Punix:
    def __init__(self,port_address="/dev/ttyUSB0",serial_dump_path="./serialdump-linux"):
        """
        Create a new object to harvest sensor information from a mote
        """
        # concat the entire command  -  the baud rate is typically 115200 so you shouldn't need to alter this
        self.fullCommand = serial_dump_path + " " + "-b115200" + " " + \
        port_address
        #handle keyboard interrupts cleanly
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self,signal, frame):
        """
        Handle signal interupts by exiting the program to ensure that all
        subprocesses end properly.
        """
        print("SIGNAL QUITTING")
        sys.exit()

    def get_sensor_data(self, duration, data_heading, print_data = True):
            """
            Harvest the sensor data for a given duration. Expects lines which
            contain data to be of the form "heading = number" where heading is
            one of the two headings in data_headings and number is a float
            containing the data being represented. Headings are also expected
            to alternate - you should never get the same heading twice.

            Returns a string containing a csv representation of the data
            captured
            """
            if print_data:
                print("Retrieving Sensor Data for",duration,"seconds")
            collected_data = "Time (seconds since epoch)," + data_heading + "\n" # data collecting during the duration

            #split string to determine the correct tokenization for 'args' to popen on unix	
            args = shlex.split(self.fullCommand)
                    
            #execute cmd as subprocess
            try:
                p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                start_time = time.time() # time that data collection started

                # Loop until the given duration time is over 
                headings = data_heading.split(",")
                while(time.time() - start_time < duration):
                        retcode = p.poll() #returns None while subprocess is running
                        line = p.stdout.readline() 
                        # Process data we want to collect
                        if line.startswith(headings[0]) or \
                           line.startswith(headings[1]): 
                            print("Seconds past since start of recording = " + str(time.time() - \
                                  start_time))
                            formatted_line = line[line.index("=")+2:].strip()
                            if line.startswith(headings[0]):
                                formatted_line = str(time.time()) + "," + \
                                                 formatted_line + ","
                            if line.startswith(headings[1]):
                                if collected_data[-1] != ",":
                                    continue
                                formatted_line = formatted_line + "\n"
                            collected_data += formatted_line

                        if(print_data):
                            sys.stdout.write(line)
                        
                        if(retcode is not None):
                            raise("Unexpected ending with retcode: " + str(retcode))

                if print_data:
                    print("\n\nShutting down sensor collection")

            finally:
                p.kill() # make sure the process ends!

            # if we have lines of data which aren't full, ignore them
            if collected_data[-1].strip() == ",":
                collected_data = collected_data[:collected_data.rindex("\n")]
            return collected_data + "\n"

if __name__ == "__main__":
    # Collect data for 5 seconds, printing all output, using the default
    # locations for ports and files
    p = Punix()
    print(p.get_sensor_data(5,"Temp,Light",True))
    
