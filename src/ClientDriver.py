from Client import Client
from Menu import *
import sys, os, datetime, argparse
DATA_TYPES = ["light","temperature","humidity"]
SERVER_DATA_LINE = "# Data from Server"
HEADER_TO_DATA_TYPE = \
{"Temp":"(\u00b0C)","Light":"(Lumens)","temperature":"(\u00b0C)","light":"(Lumens)","humidity":"(Absolute humidity)"}
def capture_data(client, write_to_file=True):
    """Prompts to allow the capturing of data
    
    if given_file_path is not empty, data will be captured to that file"""
    # user's choice for duration - must be positive
    choice = get_valid_input("How many seconds would you like to "+
            "capture data for?", 
            "Please input an positive number of seconds", 
            lambda x: x > 0, data_converter= float)
    if choice == "":
        return;
    # Get the options for data capture
    file_path = ""
    if write_to_file:
        file_path = raw_input("Please enter the file to write these results to. "+
        "Leave this line blank if you don't want results written to a file: ")
    write_to_file = not (file_path=="")

    verbose = get_user_confirmation("Do you want results to be written to screen while "+
    "recording?")
    
    # Capture the data
    return client.capture_data(choice,verbose=verbose,
                     output_to_file=write_to_file, output_path=file_path)

def render_local_data(client, file_path=""):
    """Prompts user to give location of data to be rendered into html"""
    if not file_path:
        file_path = get_valid_input("Path of results data file",
                "Please input a file that exists", 
                lambda x: os.path.isfile(x))
    if file_path=="":
        return;
    open_browser = get_user_confirmation("Do you want to open a web browser to view "+
                         " this data?") 
    print("Rendering data")
    client.generate_graph_from_data_file(file_path, open_browser=open_browser)

def upload_data(client, source_id):
    """
    Upload sensor data to the server from a variety of sources

    source_id = 0: Get the data from a local file
    source_id = 1: Get the data from a sensor
    source_id = 2: Generate the data heuristically
    """
    data = ""

    if not (0 <= source_id <= 2):
        raise ValueError("source_id not recognised")

    if(source_id == 0):
        path = get_valid_input("Path of results data file",
            "Please input a file that exists", 
            lambda x: os.path.isfile(x))
        if path=="":
            return;
        with open(path) as f:
            data = "".join(f.readlines())
    
    if(source_id == 1):
        data = capture_data(client, False)

    response = ""
    if data: 
        response = client.upload(data)
    if all([r["result"] for r in response]):
        print("Upload successful")
    return response

def get_group_data(client, group_id = -1):
    """Get the data of a specified group. 
    
    id = 0 means all groups
    id = -1 means this will prompt you to choose a valid group
    otherwise, this will try get the info for that group id
    """
    if group_id==-1: # pick group
        group_id = get_valid_input("Which group do you want to download from?"+
                                   "Give their SQL id: ",
                                   "Please input a valid id", lambda x: x > 0, int)
        if group_id == "": return;
    
    group_ids = []

    if group_id > 0: # only a single group to be downloaded
        group_ids = [group_id]
    else: # all groups need to be downloaded
        group_ids = [] # no specification means all groups 
    # download results
    response = client.download(group_ids = group_ids)
    result = response["result"]

    # allow user to see results 
    if response["result"]:
        process_download_result(result)
    return response


def get_raw_data(client):
    """Get the raw data from server"""
    # capture the groups to search for
    choice = "NOT EMPTY"
    group_ids = set()
    while str(choice).strip():
        choice = get_valid_input("Enter a group number to download",
                    "Please input a positive integer", 
                    lambda x:  x > 0,
                    int)
        if choice: group_ids.add(choice)
    if group_ids == set():
        print("No groups selected, going back to main menu")
        return;
    
    ids = sorted(list(group_ids))

    # capture times to start from or end from
    time_from = get_timestamp("Enter from what time the results must start from.")
    time_to = get_timestamp("Enter what time you want the results to end on.")
    
    # capture data types wanted
    choice = "NOT EMPTY"
    types = set()
    while str(choice).strip():
        choice = get_valid_input("Enter a data type "+
        "([T]emperature,[H]umidity,[L]ight) to download",
                    "Please input one of the letters representing choices above", 
                    lambda x: x[0].lower() in ["t","h","l"])
                    
        if choice: types.add(choice)
    if types == set():
        print("No data types selected, going back to main menu")
        return;
    # get data types from selectionsa
    types = [s.lower() for s in types]
    data_types = filter(lambda i: i[0] in types,DATA_TYPES)
    
    # only pass the parameters that aren't empty
    params = dict()
    if ids != []:
        params["group_ids"] = ids
    if time_from != "":
        params["time_from"] = time_from
    if time_to != "":
        params["time_to"] = time_to
    if data_types != []:
        params["types"] = data_types

    # download results
    response = client.download(**params)
    result = response["result"]

    # allow user to see results 
    if response["result"]:
        process_download_result(result)
    return response;

def process_download_result(result):
    """Given a result from a download request to the server, allow the user to
    save and view it"""
    if get_user_confirmation("Save to files?"):
        # format data appropriately for file writing

        # a list of the form with each entry being a list of the format "time,
        # value, group_id" for each data_type present in the list
        data = [[[str(row["time"]),str(row["value"]),str(row["group_id"])] for row in result if row["type"] == t]
                for t in DATA_TYPES]

        # a list of csv data, each representing a different type of data
        formatted_data = [(DATA_TYPES[i],"Time," + DATA_TYPES[i] + ",group_id\n" + "\n".join([",".join(row) for row
                          in data[i]])) for i in range(len(data)) if data[i] != []]

        # write the csv to files
        for pair in formatted_data:
            with open(pair[0] +" "+ str(datetime.datetime.now())+".csv","w") as f:
                f.write("# Data from Server\n"+pair[1]) 

    if get_user_confirmation("Display results?"):
            client.generate_graph_from_results(result)

def get_logs(client):
    """Get log data from the server"""
    # capture the groups to search for
    choice = "NOT EMPTY"
    group_ids = set()
    while str(choice).strip():
        choice = get_valid_input("Enter a group number to download",
                    "Please input a positive integer", 
                    lambda x: True if x == "" else x > 0,
                    lambda x: x if x=="" else int(x))
        if choice: group_ids.add(choice)
    if group_ids == set():
        print("No groups selected, going back to main menu")
        return;
    
    ids = sorted(list(group_ids))

    # capture times to start from or end from
    time_from = get_timestamp("Enter from what time the results must start from.")
    time_to = get_timestamp("Enter what time you want the results to end on")
    
    no_logs = get_valid_input("Enter a number of logs to download",
                "Please input a positive integer", 
                    lambda x: x > 0,
                    int)
    if no_logs=="":
        return;
    response =  client.get_logs(number_of_logs=no_logs,group_ids=ids,time_from=time_from,time_to=time_to)
    if response["result"]:
        result = response["result"]["lines"]
        # format data appropriately for file writing

        # a list of the form with each entry being a list of the format "time,
        # value, group_id" for each data_type present in the list
        data = [[str(row["time"]),str(row["action"]),str(row["group_id"])] for row in result]
        # a list of csv data, each representing a different type of data
        formatted_data = "time,action,group_id\n"+ "\n".join([",".join(row) for row
                          in data])

        if get_user_confirmation("Save to files?"):
                # write the csv to files
                with open("log "+ str(datetime.datetime.now())+".csv","w") as f:
                    f.write("# Log from Server\n"+formatted_data) 

        if get_user_confirmation("Display results?"):
                print(formatted_data)

def ping(client):
    """Pings the server"""
    print("ping")
    response = client.ping_server()
    if response["result"]:
        print(response["result"])
    return response

def get_aggregated_data(client, agg_type):
    """Gets aggregated data from the server of the type specified"""
    
    # capture data types wanted
    data_type = get_valid_input("Enter a data type "+
    "([T]emperature,[H]umidity,[L]ight) to download ",
                "Please input one of the letters representing choices above", 
                lambda x: x[0].lower() in ["t","h","l"])
    if data_type == "":
        print("No data types selected, going back to main menu")
        return;
    # get data types from selections
    data_type = filter(lambda i: i[0] == data_type.lower(),DATA_TYPES)[0]

    # get the group id
    group_id = get_valid_input("Enter a group number to download",
                "Please input a positive integer", 
                lambda x: x > 0,
                int)
    if group_id == "":
        print("No groups selected, going back to main menu")
        return;

    # capture times to start from and end from
    time_from = get_timestamp("Enter from what time the results must start from.")
    time_to = get_timestamp("Enter what time you want the results to end on.")


    # get and return data
    response = client.get_aggregation(agg_type, data_type, group_id,time_from, time_to)
    if response["result"]:
        print(agg_type + ":" + str(response["result"]))
    else:
        print("No data points found to make aggregation")
    return response


# Set up command line argument passing
parser = argparse.ArgumentParser(description='Set the server details')
parser.add_argument("-a",help="The address of the server. Defaults to 197.85.191.195")
parser.add_argument("-p",help="The port to connect to on the server. Defaults"+
                              " to 3000")
if __name__=="__main__":
    # setup client with arguments given from command line
    args = parser.parse_args()
    server_details = dict()
    if args.a != None:
        server_details["server_name"]= args.a
    if args.p != None:
        try:
            server_details["server_port"] = int(args.p)
        except ValueError:
            print("Error: Port not an integer. Exiting")
            sys.exit()
    client = Client(**server_details)

    while True:
        upload_screen = ("Where do you want to upload data from?",
            ("Local File","Sensor"),
            [upload_data]*2,
            [(client,i) for i in range(2)])

        download_screen = ("What data do you want to download?",
            ("Get own data","Get another group's data","Get all data","Get raw Data"),
            [get_group_data]*3+[get_raw_data],
            ((client,3),(client,-1),(client,0),[client]))
        agg_screen=("Which aggregation do you want to get?",
            ("count (how many data points)",
            "mean (average of the data points)",
            "min (minimum of the data points)",
            "max (maximum of the data points)",
            "standard deviation",
            "mode (most frequently recorded data point)",
            "median (the 'middle' data point)"),
            [get_aggregated_data]*7,
            zip([client]*7,["count","mean","min","max","std","mode","median"]))

        opening_screen = ("Welcome to Sensor Data Client! What would you like to "+
            "do?",
            ("Capture Sensor Data","Display local data",
            "Upload Data to Server","Download Data from Server","Get "+
            "Aggregated amount from Server","Get Server Logs","Ping Server","Exit"),
            [capture_data,render_local_data,execute_screen,execute_screen,execute_screen,get_logs,ping,sys.exit],
            ([client],[client],upload_screen,download_screen,agg_screen,[client],[client],[]))

        execute_screen(*opening_screen,opening=True)
