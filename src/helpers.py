import json
import requests
from datetime import datetime

# Helper functions for data processing

CITY_FILE = 'city.list.json'

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
        are missing. If searching by city name, please ensure that city was entered.
        If searching for current, local weather or forecast, please go to settings 
        and re-enter your zipcode.
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
        This most likely means that the zip code you entered does not exist or 
        the city name entered was not found. Please go to settings and ensure that 
        the zipcode you enter is correct and exists, or verify that the spelling
        of the city you entered is correct.
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
    as the city the user entered. If there are any matches put them in a list, 
    remove duplicates and return it. This could return an empty list, a list 
    with one item, or a list with multiple items
    """
    same_name_list = None
    
    # Attempt to open the file containing all the city information for the API
    try:
        with open(CITY_FILE, 'r', encoding="utf-8") as f:
            city_list = json.load(f)
    except FileNotFoundError:
        print("File Not Found: There may be an issue if there are multiple cities witht the same name.")
    else:
        #same_name_list = [city for city in city_list if city["name"] == city_input]

        """
        If the file is opened successfully check if each element loaded into 
        city_list has a particular combination of keys that is already in 
        seen. If not add the keys to the tuple key, add it to seen, and add the 
        current dictionary in city list
        """
        same_name_list = []
        seen = set()

        for city in city_list:
            if city["name"] == city_input:
                if city.get("state"):
                    key = (city["name"], city["state"], city["country"])
                    if key not in seen:
                        seen.add(key)
                        same_name_list.append(city)
                else:
                    key = (city["name"], city["country"])
                    if key not in seen:
                        seen.add(key)
                        same_name_list.append(city)
         
    return same_name_list


def verify_city_choice(city_list):
    """
    If there were multiple cities with the same name display them for the user
    and prompt them to pick a city. Return the item of the list that the user 
    selects. The item will be a dictionary of non-weather information about the
    city
    """
    print("\nThere are multiple cities matching you input.")

    for i, city in enumerate(city_list, start=1):
        print(f"Enter {i} for:")   
        print(f"\n\tCity: {city["name"]}")
        if city.get("state"):
            print(f"\tState: {city["state"]}")
        print(f"\tCountry: {city["country"]}")
        print(f"\tLatitude: {city["coord"]["lat"]}")
        print(f"\tLongitude: {city["coord"]["lon"]}\n")
    
    choice = -1
    while True:
        try:
            choice = int(input("Please select a city: ").strip())
        except ValueError:
            print("Please enter a number.")
        else:
            if choice < 1 or choice > len(city_list):
                print("Please enter a valid choice")
            else:
                break
    return city_list[choice-1]
        
           

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
        #print(len(weather_data_list))


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


def calculate_wind_direction(wind_degree):
    """
    Take the wind direction returned by the API (measured in degrees) and convert
    it to a string representation of 16 point compass (17 in the case that the
    direction is between 337.5 and 360)
    """
    wind_direction_dict = {'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90,
                           'ESE': 112.5, 'SE': 135, 'SSE': 157.5, 'S': 180, 
                           'SSW': 202.5, 'SW': 225, 'WSW': 247.5, 'W': 270, 
                           'WNW': 292.5, 'NW': 315, 'NNW': 337.5, 'N2': 360}

    min_key = None
    max_key = None
    min_dict = {}
    max_dict = {}
    
    wind_degree = wind_degree % 360
    
    # Figure out the two values that wind_degree falls between using 
    # wind_direction_dict, save the keys, and add the key
    for k, v in wind_direction_dict.items():
        if wind_degree >= v:
            min_dict[k] = v
            min_key = k
        else:
            max_dict[k] = v
            max_key = k
            break

    direction = None
    
    # Figure out which value wind_degree is closest to and save the key in the 
    # variable direction
    if wind_degree - min_dict[min_key] < max_dict[max_key] - wind_degree:
        direction = min_key
    else:
        direction = max_key

    # Since 0 and 360 is North, return 'N' id wind_degree is closer to 360
    if direction == 'N2':
        direction = 'N'

    return direction

    
