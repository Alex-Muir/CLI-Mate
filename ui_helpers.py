from datetime import datetime
import helpers

# Functions related to printing information

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
        readable_sunrise = helpers.get_sunrise(data)
        readable_sunset = helpers.get_sunset(data)

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
