"""
Some utility methods to make the operating of a menu system slightly easier
"""

def get_valid_input(msg, valid_input_msg, restriction, data_converter= lambda x: x):
   choice = None
   while choice == None:
        try:
            choice = data_converter(raw_input(msg))
            if not restriction(choice):
                choice = None
                raise ValueError()
        except ValueError:
            print(valid_input_msg)
   return choice

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


