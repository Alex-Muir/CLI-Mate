import json
import requests
from datetime import datetime
import time

FILENAME = 'settings.json'

def print_menu():
    """Print user menu"""
    print("""
    (1) Information
    (2) Settings
    (3) Get Weather
    (4) Get Forecast
    (5) Search by City
    (6) Exit""")


def print_info():
    """Print information about the application"""
    print("""
    CLI-Mate is a simple weather fetching application written in python.

    CLI-Mate uses an OpenWeatherMap API to fetch weather data. To use this app
    you must create a profile at https://home.openweathermap.org/users/sign_up.
    Once your account is created there will be an API Key sent to your email,
    which is also viewable in your profile at OpenWeatherMap.org under the 
    'API Keys'tab.

    Running CLI-Mate for the first time will automatically take you to Settings.
    Here you are greeted by a simple menu which allows you to enter you API key
    or your zipcode. This information can be changed any time.

    Once this information is entered you are ready to quickly get weather data 
    from anywhere in the United States.
    """)


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
            save_settings(settings)                                             
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
    return settings


def fetch_weather(settings):
    """Fetch current weather from OpenWeatherMap based on zip code"""                                                                     
    weather_address = f"https://api.openweathermap.org/data/2.5/weather?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(weather_address)                                           
    weather_dict = r.json()
    weather_data_list = [weather_dict]
    print_weather(weather_data_list)

def fetch_forecast(settings):
    """Fetch 5 day, 3 hour forecast from OpeWeatherMap based on zip code"""
    forecast_address = f"https://api.openweathermap.org/data/2.5/forecast?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(forecast_address)
    forecast_dict = r.json()
    weather_data_list = forecast_dict['list']
    print_weather(weather_data_list)

def get_sunrise(data):
    sys_dict = data['sys']
    sunrise_unix_UTC = sys_dict.get('sunrise')
    if sunrise_unix_UTC is None:
        return None

    readable_sunrise = datetime.fromtimestamp(sunrise_unix_UTC).time()
    return readable_sunrise

def get_sunset(data):                                                          
    sys_dict = data['sys']                                                      
    sunset_unix_UTC = sys_dict.get('sunset')                                     
    if sunset_unix_UTC is None:                                                
        return None                                                             
                                                                                
    readable_sunset = datetime.fromtimestamp(sunset_unix_UTC).time()          
    return readable_sunset  

def print_weather(weather_data_list):
    """Take relevant information from data returned by the API and print it"""
    
    for data in weather_data_list:
        # Get weather description
        weather_list = data['weather']
        weather_desc = weather_list[0]['description']

        # Get cloud coverage
        cloud_dict = data['clouds']
        cloud_coverage = cloud_dict['all']

        # Get temp related data
        temp_dict = data['main']
        current_temperature = temp_dict['temp']
        feels_like = temp_dict['feels_like']
        min_temp = temp_dict['temp_min']
        max_temp = temp_dict['temp_max']

        # Get sunrise and sunset times  
        readable_sunrise = get_sunrise(data)
        readable_sunset = get_sunset(data)

        # Get rainfall if available
        rainfall = None
        rain = data.get('rain')
        print(f"Rain Value: {rain}")
        if rain:
            rainfall = rain.get('1h')
            if rainfall is None:
                rainfall = rain.get('3h')
            

        # Get humidity and visability
        humidity = temp_dict['humidity']
        visibility = data['visibility']

        # Get wind speed and direction
        wind_dict = data['wind']
        wind_speed = wind_dict['speed']
        wind_direction = wind_dict['deg']
    
        # Get time of data calculation
        time_of_calc_unix_UTC = data['dt']
        readable_time_of_calc = datetime.fromtimestamp(time_of_calc_unix_UTC)

        # Print everything
        print(f"Weather for {readable_time_of_calc}")
        print("-" * 29)
   
        print(f"Date: {datetime.today().date()}") 
        print(f"Description: {weather_desc}")
        print(f"Current Temperature: {current_temperature}")
        print(f"Feels Like: {feels_like}")
        print(f"Min Temperature: {min_temp}")
        print(f"Max Temperature: {max_temp}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed}mph")
        print(f"Wind Direction: {wind_direction}")
        if rainfall:
            print(f"Rainfall: {rainfall}mm/h")
        print(f"Cloud Coverage: {cloud_coverage}%")
        print(f"Visibility: {visibility/1000.0}km")
        if readable_sunrise:
            print(f"Sunrise: {readable_sunrise}")
        if readable_sunset:
            print(f"Sunset: {readable_sunset}")
        print(f"\nTime of Data Calculation: {readable_time_of_calc}")

        print("-" * 29)
    
