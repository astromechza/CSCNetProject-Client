"""
Some utility methods to make the operating of a menu system slightly easier
"""

def get_valid_input(msg, valid_input_msg, restriction, data_converter= lambda x: x):
   """Prints msg until the input given can be converted to the data type given
   by the data_converter and that data satisfies the restriction function
   given. If data entered doesn't satisfy both these, print valid_input_msg"""
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

def choose_screen(msg, choices, opening=False):
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
        msg = ""
        if not opening:
            msg += "(0) Back to main screen\n"
        for i in range(1,len(choices)+1):
            msg += "("+str(i)+"): "+choices[i-1] + "\n"
        # try to get valid input
        choice = get_valid_input(msg,"Please choice a valid menu option using the "+
        "numbers on the left",lambda x: x >= 0,int)
    return choice-1 # user enters in 1-indexed value

def execute_screen(msg, choices,methods,args,opening=False):
    """An easy way to execute a choice given by a user at a particular screen"""
    choice = choose_screen(msg,choices,opening) # user choice
    if choice != -1:
        methods[choice](*args[choice]) # execute the method chosen

def get_user_confirmation(msg):
    """Get a user to either confirm or reject a request"""
    return get_valid_input(
        msg+ " (y/n) :", "Please enter either y or n", 
        lambda x: x.lower().startswith("y") or
        x.lower().startswith("n")).startswith("y")

