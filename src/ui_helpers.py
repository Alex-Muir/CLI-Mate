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
    (5) Weather by City
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
    Here you are greeted by a simple menu which allows you to enter your API key
    or your zipcode. This information can be changed any time. If nothing is 
    you will receive an error with suggestions on how to fix the problem. 

    Once this information is entered CLI-Mate is ready to fetch weather data 
    based on your desired location.  

    GET WEATHER:
        CLI-Mate's most simple option is fetching the current weather based on 
        the zipcode you entered in settings. The weather is updated every 10 
        minutes.

    GET FORECAST:
        CLI-Mate also uses OpenWeather's 5 day, 3 hour forecast to give you up
        to 40 different forecasts (the forecast reports weather at 3 hour
        intervals for 5 24 hour periods) based on your zipcode. When selecting 
        this option you will be prompted to select the desired forecast for a 
        particular day or print all the available forecasts.

    WEATHER BY CITY:
        CLI-Mate has the option to get the current weather anywhere in the world
        that is in OpenWeather's database. When selecting this option you will 
        be prompted to enter a city. If the name of the city entered has multiple 
        matches in different countries or U.S. states you  will be promted to
        select the desired city from a list of possible options.

    A Note About Output:
        All output is currently in imperial measurments, except for visibility, 
        which is only available in metric. 

        Some output only appears when it is relevant to the weather. For example, 
        rain and snow will not appear in the output if it is not raining or 
        snowing, or none is predicted. 

        Temperature Variance is the difference in possible temperatures for the 
        given area at the time of the last update. Often when using the 'Get 
        Forecast' option temperature variance is not updated which gives the 
        output of +0.0 and -0.0. 

        Lastly, Sunrise and Sunset does not appear in the output for the 'Get 
        Forecast'.

    Bugs:
        Please report bugs at https://github.com/Alex-Muir/CLI-Mate/issues
    """)


def print_weather(weather_data_list, name=""):
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
        min_var = current_temperature - min_temp
        max_var = max_temp - current_temperature

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
        
        snowfall = None                                                         
        snow = data.get('snow')                                                 
                                                                             
        if snow:                                                                
            snowfall = snow.get('1h')                                           
            if snowfall is None:                                                
                snowfall = snow.get('3h')     

        # Get humidity and visability
        humidity = temp_dict['humidity']
        visibility = data.get("visibility")

        # Get wind speed and direction
        wind_dict = data['wind']
        wind_speed = wind_dict['speed']
        wind_direction = wind_dict['deg']

        # Get time of data calculation
        time_of_calc_unix_UTC = data['dt']
        readable_time_of_calc = datetime.fromtimestamp(time_of_calc_unix_UTC)

        city_name = data.get("name")
        if city_name is None:
            city_name = name

        # Print everything
        print(f"\nWEATHER for {city_name.upper()} - {readable_time_of_calc}")
        print("-" * 29)
   
        print(f"Date: {datetime.today().date()}") 
        print(f"Description: {weather_desc}")
        print(f"Current Temperature: {current_temperature}")
        print(f"Feels Like: {feels_like}")
        print(f"Temperature Variance: +{round(max_var, 1)}, -{round(min_var, 1)}")
        #print(f"Min Temperature: {min_temp}")
        #print(f"Max Temperature: {max_temp}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed}mph")
        print(f"Wind Direction: {helpers.calculate_wind_direction(wind_direction)}")
        if rainfall:
            print(f"Rainfall: {rainfall}mm/h")
        if snowfall:
            print(f"Snowfall: {snowfall}mm/h")
        print(f"Cloud Coverage: {cloud_coverage}%")
        if visibility:
            print(f"Visibility: {visibility/1000.0}km")
        if readable_sunrise:
            print(f"Sunrise: {readable_sunrise}")
        if readable_sunset:
            print(f"Sunset: {readable_sunset}")
        print("-" * 29)
