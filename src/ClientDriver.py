from Client import Client
import sys
def choose_screen(msg, choices):
    """
    An easy way to allow a user to choice an option from a screen

    It takes a screen, a a message to print to the
    user and a series of choices, and returns the index of the choice
    chosen by the user
    """
    print(msg) 
    choice = -1 # the option the user chooses
    while(choice < 0):
        # print options
        for i in range(1,len(choices)+1):
            print "("+str(i)+") :",choices[i-1]
        # try to get valid input
        try:
            choice = int(raw_input());
            if not (0 < choice <= len(choices)):
                choice = -1
                raise ValueError()
        except ValueError:
            print ("Choice not a valid integer")
    return choice-1 # user enters in 1-indexed value

def execute_screen(msg, choices,methods,args):
    """An easy way to execute a choice given by a user at a particular screen"""
    choice = choose_screen(msg,choices) # user choice
    methods[choice](*args[choice]) # execute the method chosen

def capture_data(client):
    """Prompts to allow the capturing of data"""
    choice = -1 # user's choice for duratino
    while(choice < 0):
        # keep repeating until positive number choice attained
        try:
            choice = int(raw_input("How many seconds would you like to "+
            "capture data for: "))
            if choice < 0:
                raise ValueError()
        except ValueError:
            print("Please input an positive number of seconds")

    # Get the options for data capture
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
    file_path = raw_input("Path of results data file: ")
    #TODO: replace y/n getting with method
    open_browser = raw_input("Do you want to open a web browser to view "+
                             " this data? (y/n)").lower().startswith("y")
    client.generate_graph_from_data_file(file_path, open_browser=open_browser)

def upload_data(client, source_id):
    """
    Upload sensor data to the server from a variety of sources

    source_id = 0: Get the data from a local file
    source_id = 1: Get the data from a sensor
    source_id = 2: Generate the data heuristically
    """
    pass


def get_data(client, group_id = -1):
    """Get the data of a specified group. 
    
    id = 0 means all groups
    id = -1 means this will prompt you to choose a valid group
    otherwise, try get the info for that group id
    """
    pass

def get_raw_data(client):
    """Get the answer to a raw SQL query"""
    pass

def get_logs(client,log_type):
    """
    Get log data from the server
    log_type = 0: All logs
    log_type = 1: Uploading logs
    log_type = 2: Downloading logs
    """
    pass

if __name__=="__main__":
    client = Client()
    while True:
        upload_screen = ("Where do you want to upload data from?",
            ("Local File","Sensor","Data Generated Heuristically"),
            [upload_data]*3,
            [(client,i) for i in range(3)])

        download_screen = ("What data do you want to download?",
            ("Get own data","Get another group's data","Get all data","Get raw Data"),
            [get_data]*3+[get_raw_data],
            ((client,2),(client,-1),(client,0),(client)))

        get_log_screen = ("What log information do you want?",
            ("All the logs", "All the upload logs", "All the download logs"),
            [get_logs]*3,
            [(client,i) for i in range(3)])

        opening_screen = ("Welcome to Sensor Data Client! What would you like to "+
            "do?",
            ("Capture Sensor Data","Display local data","Upload Data to Server","Download Data from Server","Get Server Logs","Exit"),
            [capture_data,render_local_data,execute_screen,execute_screen,execute_screen,sys.exit],
            ([client],[client],upload_screen,download_screen,get_log_screen,()))
        execute_screen(*opening_screen)
