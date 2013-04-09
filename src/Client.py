import json, webbrowser, os, datetime, csv
from punix import Punix
from socket import *

RESULTS_DATA_PATH = "templates/results.html"
GRAPH_DATA_PATH = "templates/graph.js"
RESULTS_JSON_STRING = "@JSON_QUERY_DATA_STRING"
RESULTS_FOOTER = "@FOOTER_CONTENTS"
QUERY_NUMBER = "@QUERY_NUMBER"
CONTAINER_TOKEN = "@CONTAINER_CONTENTS"
GRAPH_TOKEN = "@HIGHCHARTS_SETUP"
DATA_TYPES = {"Temp":"(\u00b0C)","Light":"(Lumens)"}
HEADING_TO_FULL_NAME = {"Temp":"temperature","Light":"light"}
class Client:
 
    def __init__(self, server_name = "197.85.191.195", server_port = 3000,
    group_id=2):
        self.server_name = server_name
        self.server_port = server_port
        self.port_address="/dev/ttyUSB0"
        self.serial_dump_path="./serialdump-linux"
        self.headings = "Temp,Light"
        self.group_id = group_id
    
    def generate_graph_from_data_file(self, path, open_browser=False,
    feedback=True):
        """
        Given a csv file created from sensor data captured using this client,
        generate graphs representing its data
        """
        with open(path) as f:
            headers = f.readline().split(",") # first line of csv is headers
            indep_var = headers[0].strip() # independant variable  
            dep_var = [i.strip() for i in headers[1:]]  # dependant variables
            data = [line.strip().split(",") for line in f.readlines()]
            dates = [row[0] for row in data]
            self.generate_graphs(data=
                        [
                            {"dates":dates,
                            "data":[{"name":"Data recorded by Collection 3",
                                     "data":[float(row[i+1]) for row in data]}],
                            "y_axis_legend": dep_var[i],
                            "title": dep_var[i]+ " of Data Recorded",
                            "subtitle": "Source: Collection 3 Data",
                            "data_type":DATA_TYPES[dep_var[i]]}
                        for i in range(len(dep_var))],
                    open_browser=open_browser,feedback=feedback)

    def generate_graphs(self,data=[],open_browser=False,feedback=True):
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

        graph_source = "" # the source code for the graph js
        with open(GRAPH_DATA_PATH) as f:
            for line in f:
                graph_source += line;

        contents_code = "" # the code to insert into the contents token
        graph_code = "" # the code to insert into the graph token
        for i in range(len(data)):
            contents_code +=("<div id= graph_%i></div>")%(i)
            graph_code += graph_source.replace(QUERY_NUMBER,str(i))

        results = "" # the full html and js to put into the results page
        with open(RESULTS_DATA_PATH,"r") as f:
            for line in f:
                results += line

        # insert the relevant js and text into the results page html
        replace_pairs = ((RESULTS_JSON_STRING,"'"+json.dumps(data)+"'"),
                        (RESULTS_FOOTER,"Generated at " +str(datetime.datetime.now())),
                        (CONTAINER_TOKEN, contents_code),
                        (GRAPH_TOKEN, graph_code))
        for a,b in replace_pairs:
            results = results.replace(a,b)
        with open("results.html","w") as f:
            f.write(results)

        # open the results page in a browser if wanted
        if open_browser:
            if feedback:
                print("Attempting to open web browser. If this fails, manually "+
                "open results.html")
            dir_path = os.path.split(os.path.realpath(__file__))[0]
            results_path = os.path.join(dir_path,"results.html")
            url = "file://"+results_path
            webbrowser.open_new_tab(url)
        else: 
            if feedback:
                print("Results saved as results.html. Please open with a web browser"+
                " to view.")

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

    def upload(self, data):
        """Uploads the data to the stored server"""
        lines = data.split("\n")
        csvreader = csv.reader(lines, delimiter=',', quotechar='"')
        csvreader.next() # skip headers
        types = [HEADING_TO_FULL_NAME[h.strip()] for h in lines[0].split(",")[1:]]
        results = []
        # TODO: do this in increments of 100s to make give user feedback
        for row in csvreader:
            if row: # skip empty rows
                for i in range(1,3):
                    results.append({"time":int(float(row[0])*1000),"type":types[i-1],"value":float(row[i])})

        return self.send_data("new_readings",{"readings":results})

    def download(self,group_ids = [1], time_from="", time_to="",
                 types = ["light","temperatures","humidity"]):
        """Fetches all records for a given query from the server"""
        params ={"group_ids":group_ids,"types":types}
        if time_from != "":
            params["time_from"] = time_from
        if time_to != "":
            params["time_to"] = time_to
        return self.send_data("query_readings",params)

    def get_logs(self,log_type):
        """
        Get log data from the server
        log_type = 0: All logs
        log_type = 1: Uploading logs
        log_type = 2: Downloading logs
        """
        # TODO
        print ("log download still needs to be implemented")

    def send_data(self,method,params,verbose=False):
        """Send data over a socket"""
        query = json.dumps({"method":method,"params":params, "group_id":self.group_id})
        client_socket = socket(AF_INET, SOCK_STREAM)
        if verbose:
            print("Socket made")
            print("Connecting to Server")
        client_socket.connect((self.server_name, self.server_port))
        if verbose:
            print("Connected to Server")
            print("Sending info")
        client_socket.send(query+"\n")
        if verbose: 
            print("Sent info")
            print("Receiving data")
        reply = []
        running = True
        while running:
                data = client_socket.recv(1024)
                reply.append(data)
                if data.endswith("\n"): # json terminates with \n
                    running = False
        client_socket.close()
        if verbose:
            print("Received data, closed socket")
        return json.loads("".join(reply))

    def ping_server(self):
        """Pings the server to ensure connection is possible"""
        return self.send_data("ping",[])
        


