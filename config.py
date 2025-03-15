import json

# Functions related to user settings

FILENAME = 'settings.json'

def set_settings(settings):
    """Display menu options for settings. Take user input for settings and save"""                               
    while True:                                                                 
        print("(1) Enter an API key\n(2) Enter your zip code\n(3) Exit")        
        choice = input("What would you like to do? ")                           
        if choice == '1':                                                       
            settings["API_KEY"] = input("Enter your API key: ")                 
        elif choice == '2':                                                     
            settings["zip_code"] = input("Enter your zip code: ")               
        elif choice == '3':                                             
            break                                                               
        else:                                                                   
            print("Please enter a valid selection")  
                                                                                  
    return settings


def save_settings(settings):
    """Save user settings to a text file in json format""" 
    try:                                                                        
        with open(FILENAME, 'w') as f:                                          
            json.dump(settings, f)                                              
    except FileNotFoundError:                                                   
        print("There is an issue with the file")                                
    else:                                                                       
        print("File saved")


def load_settings():
    """Load user settings from text file and store them in a dictionary"""
    
    try:                                                                        
        with open(FILENAME, 'r') as f:                                          
            settings = json.load(f)                                             
    except FileNotFoundError:                      
        print("It seems that setting have not been entered. Please enter them now.")
        default_settings = {"API_KEY": "", "zip_code": ""}                      
        settings = set_settings(default_settings)
        save_settings(settings)   
    print(settings)                                              
    return settings
