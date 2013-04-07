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
    client.capture_data(choice,verbose=verbose,
                     output_to_file=write_to_file, output_path=file_path)

if __name__=="__main__":
    while True:
        opening_screen = ("Welcome to Sensor Data Client! What would you like to "+
        "do?",(["Capture Sensor Data","Exit"]),[capture_data,sys.exit],[[Client()],[]])
        execute_screen(*opening_screen)
