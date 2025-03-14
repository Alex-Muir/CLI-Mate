import json
import requests
from datetime import datetime
import time

FILENAME = 'settings.json'
CITY_FILE = 'city.list.json'

def print_menu():
    """Print user menu"""

    print("\nCLI-Mate")
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


def verify_response(status_code):
    """
    Verify that the response from the API is good. If it is not, print the 
    possible reason and aid the user in correcting the problem
    """

    if status_code == 200:                                                    
        return True                                                        
    elif status_code == 400:                                                  
        print("""
        ERROR: It is possible that some of the required parameters for the request 
        are missing. Please go to settings and re-enter your zipcode.
        """)                                                                                                                         
    elif status_code == 401:                                                  
        print("""
        ERROR: There is an issue with the API Key. It is either incorrect or the 
        key that was entered does not give access to the API for this application. 
        Either re-enter the key in settings, or verify that the key you have 
        entered gives access to OpenWeatherMap's Current Weather and 5 day, 3 
        hour API.
        """)                                       
    elif status_code == 404:                                                  
        print("""
        ERROR: A parameter in the request does not exist in the service database. 
        This most likely means that the zip code you entered does not exist. 
        Please go to settings and ensure that the zipcode you enter is correct 
        and exists.
        """)    
    elif status_code == 429:                                                  
        print("""
        ERROR: It appears the key quota has been exceeded for this API. Please 
        try your request again later.
        """)                                                                                                     
    elif status_code >= 500:                                                  
        print("""
        ERROR: This is most likely caused by an internal error. Please consider 
        conatcting OpenWeather and enclosing the API key causing this issue.
        """)                                                    

    return False


def same_name_cities(city_input):
    """
    Check to see if there are multiple cities in the database with the same name
    as the city the user entered. If there are any matches put them in a list 
    and return it. This could return an empty list, a list with one item, or a 
    list with multiple items
    """
    same_name_list = None
    try:
        with open(CITY_FILE, 'r') as f:
            city_list = json.load(f)
    except FileNotFoundError:
        print("File Not Found: There may be an issue if there are multiple cities witht the same name.")
    else:
        same_name_list = [city for city in city_list if city["name"] == city_input]
        #print(same_name_list) 
    return same_name_list


def verify_city_choice(city_list):
    """
    If there were multiple cities with the same name display them for the user
    and prompt them to pick a city. Return the item of the list that the user 
    selects. The item will be a dictionary of non-weather information about the
    city
    """
    print("There are multiple cities matching you input.")

    for i, city in enumerate(city_list, start=1):
        print(f"Enter {i} for:")   
        print(f"\tCity: {city["name"]}")
        if city.get("state"):
            print(f"\tState: {city["state"]}")
        print(f"\tCountry: {city["country"]}\n")
    
    choice = -1
    while True:
        try:
            choice = int(input("Please select a city: "))
        except ValueError:
            print("Please enter a number.")
        else:
            if choice < 1 or choice > len(city_list):
                print("Please enter a valid choice")
            else:
                break
    return city_list[choice-1]
        
           
def fetch_weather(settings):
    """Fetch current weather from OpenWeatherMap based on zip code"""                                                                     
    weather_address = f"https://api.openweathermap.org/data/2.5/weather?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(weather_address) 
    verified = verify_response(r.status_code)
    if verified:                         
        weather_dict = r.json()
        weather_data_list = [weather_dict]
        print_weather(weather_data_list)


def fetch_forecast(settings):
    """Fetch 5 day, 3 hour forecast from OpeWeatherMap based on zip code"""
    forecast_address = f"https://api.openweathermap.org/data/2.5/forecast?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(forecast_address)
    verified = verify_response(r.status_code)
    if verified:
        forecast_dict = r.json()
        weather_data_list = forecast_dict['list']
        initial_size = len(weather_data_list)
        prompt = "Do you want to select a particular date?"
        prompt += "\nEnter 'y' for yes, anything else to print all forecast data: "
        refine_date(weather_data_list, prompt)
        print_weather(weather_data_list)


def weather_by_city(settings):
    """Attempt to get the weather of a particular city entered by the user"""
    city = input("Enter city name: ").strip().title()

    city_list = same_name_cities(city)
    print(city_list)
    
    city_choice_dict = None
    if len(city_list) > 1:
        city_choice_dict = verify_city_choice(city_list)

    #print(city)
    city_address = f"https://api.openweathermap.org/data/2.5/weather?q={city}"
    if city_choice_dict:
        if city_choice_dict.get("state"):
            city_address += f",{city_choice_dict["state"]}"
        city_address += f",{city_choice_dict["country"]}"
    city_address += f"&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(city_address)
    verified = verify_response(r.status_code)
    if verified:
        city_dict = r.json()
        #print(city_dict)
        weather_data_list = [city_dict]
        print_weather(weather_data_list) 

def refine_date(weather_data_list, prompt):
    """
    Get every unique date from the list of weather data and prompt the user
    for a particular day, or all data. Change the list of weather data in 
    place to reflect the chosen date for the forecast.
    """ 
    choice = input(prompt)
    choice_list = []

    if choice.lower() == 'y':

        # add each unique date to choice_list 
        for i in range(len(weather_data_list)):

            # convert the unix UTC time to a local, readable date
            date = datetime.fromtimestamp(weather_data_list[i]['dt']).date()
            if date not in choice_list:
                choice_list.append(date)
        
        # print the menu for the date selection by the user
        for i, time in enumerate(choice_list, start=1):
            print(f"({i}) {choice_list[i-1]}")
        
        while True:
            try:
                choice = int(input("Enter your selection: "))
            except ValueError:
                print("Please enter a valid selection.")
            else:
                if choice > len(choice_list) or choice <= 0:
                    print("Please enter a valid selection")
                else:
                    break
        date_selected = choice_list[choice-1]

        # Change list in place. Add all forecast data to the list where the date
        # matches the user's choice
        weather_data_list[:] = [forecast for forecast in weather_data_list if datetime.fromtimestamp(forecast['dt']).date() == date_selected]
        print(len(weather_data_list))


def get_sunrise(data):
    """Get sunrise from fetched data for current weather or forecast"""
    sys_dict = data['sys']
    sunrise_unix_UTC = sys_dict.get('sunrise')
    if sunrise_unix_UTC is None:
        return None

    readable_sunrise = datetime.fromtimestamp(sunrise_unix_UTC).time()
    return readable_sunrise

def get_sunset(data):
    """Get sunset from fetched data for current weather or forecast"""        
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
        print(f"\nWeather for {readable_time_of_calc}")
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
    
