from Client import Client
from Menu import choose_screen, execute_screen, get_valid_input
import sys
import os
#TODO: error checking networking requests
def capture_data(client, write_to_file=True):
    """Prompts to allow the capturing of data
    
    if given_file_path is not empty, data will be captured to that file"""
    # user's choice for duration - must be positive
    choice = get_valid_input("How many seconds would you like to "+
            "capture data for: ", 
            "Please input an positive number of seconds", 
            lambda x: x > 0, data_converter= float)

    # Get the options for data capture
    file_path = ""
    if write_to_file:
        file_path = raw_input("Please enter the file to write these results to. "+
        "Leave this line blank if you don't want results written to a file: ")
    write_to_file = not (file_path=="")
    verbose = raw_input("Do you want results to be written to screen while "+
    "recording? (y/n): ").lower().startswith("y")
    
    # Capture the data
    return client.capture_data(choice,verbose=verbose,
                     output_to_file=write_to_file, output_path=file_path)

def render_local_data(client):
    """Prompts user to give location of data to be rendered into html"""
    file_path = get_valid_input("Path of results data file: ",
            "Please input a file that exists", 
            lambda x: os.path.isfile(x))
    
    open_browser = get_valid_input("Do you want to open a web browser to view "+
                         " this data? (y/n)", "Please enter either y or n", 
                         lambda x: x.lower().startswith("y") or
                         x.lower().startswith("n")).startswith("y")
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
        path = get_valid_input("Path of results data file: ",
            "Please input a file that exists", 
            lambda x: os.path.isfile(x))
        with open(path) as f:
            data = "".join(f.readlines())
    
    if(source_id == 1):
        data = capture_data(client, False)

    response = ""
    if data: 
        response = client.upload(data)
    print(response["result"])
    return response

def get_data(client, group_id = -1):
    """Get the data of a specified group. 
    
    id = 0 means all groups
    id = -1 means this will prompt you to choose a valid group
    otherwise, this will try get the info for that group id
    """
    # TODO support more granular group selection
    if group_id==-1:
        group_id = get_valid_input("Which group do you want to download from?"+
                                        "Give their SQL id.",
                                    "Please input a valid id", lambda x: x >= 0, int)
    group_ids = []
    if group_id > 0:
        group_ids = [group_id]
    else:
        group_ids = [1,2,3] #TODO: make this a bit more general
    response = client.download(group_ids = group_ids, types = ["light","temperatures","humidity"])
    print(response["result"])
    return response

def get_raw_data(client):
    """Get the raw data from server"""
    query = raw_input("What do you want to get from the server? #TODO: figure"+
    " out wtf raw data is")
    return client.download(query)

def get_logs(client):
    """Get log data from the server"""
    print("TODO")

def ping(client):
    """Pings the server"""
    print("ping")
    response = client.ping_server()
    print(response["result"])
    return response

if __name__=="__main__":
    client = Client()
    while True:
        upload_screen = ("Where do you want to upload data from?",
            ("Local File","Sensor"),
            [upload_data]*2,
            [(client,i) for i in range(2)])

        download_screen = ("What data do you want to download?",
            ("Get own data","Get another group's data","Get all data","Get raw Data"),
            [get_data]*3+[get_raw_data],
            ((client,2),(client,-1),(client,0),(client)))

        opening_screen = ("Welcome to Sensor Data Client! What would you like to "+
            "do?",
            ("Capture Sensor Data","Display local data","Upload Data to Server","Download Data from Server","Get Server Logs","Ping Server","Exit"),
            [capture_data,render_local_data,execute_screen,execute_screen,get_logs,ping,sys.exit],
            ([client],[client],upload_screen,download_screen,[client],[client],[]))

        execute_screen(*opening_screen,opening=True)
