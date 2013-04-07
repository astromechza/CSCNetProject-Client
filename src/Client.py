import json, webbrowser, os, datetime
from punix import Punix
RESULTS_DATA_PATH = "templates/results.html"
GRAPH_DATA_PATH = "templates/graph.js"
RESULTS_JSON_STRING = "@JSON_QUERY_DATA_STRING"
RESULTS_FOOTER = "@FOOTER_CONTENTS"
QUERY_NUMBER = "@QUERY_NUMBER"
CONTAINER_TOKEN = "@CONTAINER_CONTENTS"
GRAPH_TOKEN = "@HIGHCHARTS_SETUP"
class Client:
    def __init__(self):
        self.port_address="/dev/ttyUSB0"
        self.serial_dump_path="./serialdump-linux"
        self.headings = "Temp,Light"

    def generate_graphs(self,data=[],open_browser=False):
        """
        Generate the json output required to render a line graph with highcharts.js
        
        Takes an array of dictionaries with entries:
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
        graph_source = ""
        with open(GRAPH_DATA_PATH) as f:
            for line in f:
                graph_source += line;
        contents_code = ""
        graph_code = ""
        for i in range(len(data)):
            contents_code +=("<div id= graph_%i></div>")%(i)
            graph_code += graph_source.replace(QUERY_NUMBER,str(i))

        results = ""
        with open(RESULTS_DATA_PATH,"r") as f:
            for line in f:
                results += line
        replace_pairs = ((RESULTS_JSON_STRING,"'"+json.dumps(data)+"'"),
                        (RESULTS_FOOTER,"Generated at " +str(datetime.datetime.now())),
                        (CONTAINER_TOKEN, contents_code),
                        (GRAPH_TOKEN, graph_code))
        for a,b in replace_pairs:
            results = results.replace(a,b)

        with open("results.html","w") as f:
            f.write(results)

        if open_browser:
            print("Attempting to open web browser. If this fails, manually "+
            "open results.html")
            dir_path = os.path.split(os.path.realpath(__file__))[0]
            results_path = os.path.join(dir_path,"results.html")
            url = "file://"+results_path
            #webbrowser.open_new_tab(url)
        else: 
            print("Results saved as results.html. Please open with a web browser"+
            " to view")

    def capture_data(self,duration,verbose=False,
                     output_to_file=False, output_path=""):
        """
        Given a port and a time to catch data for, capture data from a mote
        connected to the computer and dump it to a text file on the computer
        """
        p = Punix(self.port_address,self.serial_dump_path)
        data = ""
        try:
            data =  p.get_sensor_data(duration,self.headings,print_data=verbose)
            if(output_to_file):
                with open(output_path,"w") as f:
                    f.write(data)
        except OSError:
            print("Error: Could not capture data. Check sensor is connected "+
            "and that this is running with the correct permissions")
        return data
