import json, webbrowser, os, datetime, csv, time
from punix import Punix
from socket import *

#RESULTS_DATA_PATH = "templates/results.html"
RESULTS_DATA_PATH = "templates/stocks_results.html"
#GRAPH_DATA_PATH = "templates/graph.js"
GRAPH_DATA_PATH = "templates/stocks_graph.js"
RESULTS_JSON_STRING = "@JSON_QUERY_DATA_STRING"
RESULTS_FOOTER = "@FOOTER_CONTENTS"
QUERY_NUMBER = "@QUERY_NUMBER"
CONTAINER_TOKEN = "@CONTAINER_CONTENTS"
GRAPH_TOKEN = "@HIGHCHARTS_SETUP"
HEADER_TO_DATA_TYPE = \
{"Temp":"(\u00b0C)","Light":"(Lumens)","temperature":"(\u00b0C)","light":"(Lumens)","humidity":"(Absolute humidity)"}
HEADING_TO_FULL_NAME = {"Temp":"temperature","Light":"light"}
SERVER_DATA_LINE = "# Data from Server"

class Client:
    def __init__(self, server_name = "197.85.191.195", server_port = 3000,
    group_id=2):
        self.server_name = server_name
        self.server_port = server_port
        self.port_address="/dev/ttyUSB0"
        self.serial_dump_path="./serialdump-linux"
        self.headings = "Temp,Light"
        self.group_id = group_id

    def generate_graph_from_results(self,result, open_browser=False):
        """
        Given an arrray of dictionaries of the form
            {
            * 'group_ids' : integer representing the group number,
            * 'value' => the value of the reading,
            * 'type' => string of type,
            * 'time' => iso date string
            * }
        Generate a graphs representing the data
        """
        # find all data_types present in the data
        data_types_present = {row["type"] for row in result}
        
        print(str(data_types_present))
        # find all the groups present in the data
        group_ids = {row["group_id"] for row in result}
        # for each group, creat a graph representing its data
        
        data_to_graph = []
        for data_type in data_types_present:
            
            graph_info = {
                "dates": [row["time"] for row in result if row["type"]==data_type],
                "title": data_type,
                "data_type": data_type +" "+ HEADER_TO_DATA_TYPE[data_type]
            }
            
            series_data = []
            for g_id in group_ids:
                series = {"name": "Group " + str(g_id)}
                dates_used = set()
                data = []
                for row in result:
                    if (row["group_id"] == g_id and row["type"] == data_type and (row['time'] not in dates_used)):
                        date = row['time']
                        try:
                            date= float(date)*1000 # wants milliseconds
                        except ValueError:
                            if(date.find(".") != -1):
                                # database doesn't store milliseconds, so remove
                                # them
                                date = date[:date.find(".")] 
                            date = time.mktime(time.strptime(date,"%Y-%m-%d %H:%M:%S"))
                            date *= 1000 # wants milliseconds
                            date = int(date)
                    
                        data.append([date, row['value']])
                        dates_used.add(row['time'])
                series["data"] = data
                series_data.append(series)             
            
 
            graph_info["data"] = series_data
            del graph_info["dates"]
            data_to_graph.append(graph_info)
        
        # Generate the graphs
        self.generate_graphs(data=data_to_graph,open_browser=True,feedback=True)
        

    def generate_graph_from_data_file(self, path, open_browser=False,
    feedback=True):
        """
        Given a csv file created from sensor data captured using this client,
        generate graphs representing its data
        """
        with open(path) as f:
            first_line = f.readline()

            # as sensor csv files and data files downloaded from the server
            # have different data formats, we must differentiate between them.

            # A better solution would be to standardise the data format, but as
            # we don't have access to the sensors, we don't want to possibly
            # break the code that deals with them and so we have to keep this
            # legacy code.
            if first_line.strip() == SERVER_DATA_LINE.strip():
                headers = f.readline().split(",") # first line of csv is headers

                data_type = headers[1].strip() # middle value is always data
                                               # type

                csvreader = csv.reader(f.readlines(), delimiter=',', quotechar='"')

                # since this was generated from a download server result, let's
                # reformat this data like a server result and use that to graph
                # it
                result = [{"group_id":row[2].strip(),
                           "value":float(row[1].strip()),
                           "type":data_type,
                           "time":row[0].strip()} for row in csvreader]

                self.generate_graph_from_results(result,open_browser)
            else: # Sensor data 
                headers = first_line.split(",") # first line of csv is headers
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
                                "data_type":dep_var[i] + " " + HEADER_TO_DATA_TYPE[dep_var[i]]}
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
        # due to the fact that mysql doesn't support milliseconds in iso time
        # and some groups have multiple reads per second, we have to filter out
        # some readings in order to make sure the graphs can be displayed. As
        # the readings are taken in the same place as they're the same sensor,
        # we can assume that the readings aren't really going to change. The
        # other fix is to change the server side to take time as a long, but as
        # this would break other client's the most sensible change, with almost
        # no impact to the actual conclusions that can be taken to the
        # readings, is just making sure there's only one value per second.


        graph_source = "" # the source code for the graph js
        with open(GRAPH_DATA_PATH) as f:
            for line in f:
                graph_source += line;

        contents_code = "" # the code to insert into the contents token
        graph_code = "" # the code to insert into the graph token
        for i in range(len(data)):
            contents_code +=("<div> <h2>"+data[i]["title"]+"</h2></div><div id= graph_%i></div>")%(i)
            graph_code += graph_source.replace(QUERY_NUMBER,str(i))

        results = "" # the full html and js to put into the results page
        with open(RESULTS_DATA_PATH,"r") as f:
            for line in f:
                results += line

        # insert the relevant js and text into the results page html
        replace_pairs = ((RESULTS_JSON_STRING,json.dumps(data)),
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
        for row in csvreader:
            if row: # skip empty rows
                for i in range(1,3):
                    results.append({"time":int(float(row[0])*1000),"type":types[i-1],"value":float(row[i])})

        return self.send_data("new_readings",{"readings":results})

    def download(self,group_ids = [], time_from="", time_to="",
                 types = ["light","temperature","humidity"]):

        """Fetches all records for a given query from the server"""
        params ={"types":types}
        if group_ids != []:
            params["group_ids"] = group_ids
        if time_from != "":
            params["time_from"] = time_from
        if time_to != "":
            params["time_to"] = time_to
        print(str(params))
        return self.send_data("query_readings",params)

    def get_logs(self,number_of_logs=20,group_ids=[],time_from="",time_to=""):
        """Get log data from the server"""
        params = {"limit":number_of_logs}
        if group_ids:
            params["group_ids"] = group_ids
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to
        return self.send_data("query_logs",params)

    def send_data(self,method,params,verbose=False):
        """Send data over a socket"""
        # setup data for transfer
        query = json.dumps({"method":method,"params":params, "group_id":self.group_id})
        client_socket = socket(AF_INET, SOCK_STREAM) # set socket to TCP
        client_socket.settimeout(5) # to make sure client doesn't wait eternally
        reply = [] # the lines of reply the server sends back

        try:
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
            running = True
            while running:
                    data = client_socket.recv(1024)
                    reply.append(data)
                    if data.endswith("\n"): # json terminates with \n
                        running = False
            if verbose:
                print("Received data, closed socket")
        except timeout:
            print("Error: Connection timed out")

        except gaierror as e:
            print("Gai error({0}): {1}".format(e.errno,e.strerror))
        
        except error as e: # socket error:
            print("Socket error({0}): {1}".format(e.errno,e.strerror))
        finally:
            client_socket.close()

        response = {}
        if reply: # data received, load object send
            response = json.loads("".join(reply))
        else: # data not recieved, default to error
            response = {"result":"","error":"No response from server"}

        if "error" in response: # client has given an error
            print("Error from server: " + response["error"])

        if "result" in response:
            if response["result"] == "":
                print("No result to process from Server")
        return response

    def ping_server(self):
        """Pings the server to ensure connection is possible"""
        return self.send_data("ping",[])

    def get_aggregation(self, aggregation_type, data_type, group_id=None,
                        time_from="", time_to=""):
        """Fetches aggregated versions of data"""
        params = {"aggregation":aggregation_type, "type":data_type}
        if group_id != None:
            params["group_id"] = group_id
        if time_from != "":
            params["time_from"] = time_from
        if time_to != "":
            params["time_to"] = time_to
        return self.send_data("aggregate",params)
