import json
from punix import Punix
QUERY_DATA_PATH = "query_data.json"
QUERY_DATA_PREAPPEND = "query_data="
class Client:
    def generate_results(self,dates=[],data= [{"name":"",
    "data":[]}],y_axis_legend="",title="",subtitle="",data_type=""):
        """
        Generate the json output required to render a line graph with highcharts.js

        dates: array of strings naming the points on the x-axis the data points
        will correspond to
        data: an array of dictionaries of the form {"name:"",data:[]} where name is
        the name of the particular dataset (e.g. Group 1's data) and data is an
        array of data points corresponding in order to the dates given.
        y_axis_legend: the legend to put on the y-axis
        title: title of the graph
        subtitle: the subtitle to give the graph
        data_type: the data type the graph is showing, e.g. degrees celsius.
        """
        data_dict = {"dates":  dates,
        "data": data,
        "y_axis_legend" : y_axis_legend,
        "title" :title,
        "subtitle" : subtitle,
        "data_type" : data_type}
        with open(QUERY_DATA_PATH,"w") as f:
            f.write(QUERY_DATA_PREAPPEND + json.dumps(data_dict))


    def capture_data(self,duration,port_address="/dev/ttyUSB0",
                     serial_dump_path="./serialdump-linux",verbose=False):
        """
        Given a port and a time to catch data for, capture data from a mote
        connected to the computer and dump it to a text file on the computer
        """
        p = Punix(port_address,serial_dump_path)
        return p.get_sensor_data(duration,"Temp,Light",print_data=verbose)
