import requests
import ui_helpers
import helpers

# Functions related to the OpenWeather API

def fetch_weather(settings):
    """Fetch current weather from OpenWeatherMap based on zip code"""                                                                     
    weather_address = f"https://api.openweathermap.org/data/2.5/weather?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(weather_address) 
    verified = helpers.verify_response(r.status_code)
    if verified:                         
        weather_dict = r.json()
        weather_data_list = [weather_dict]
        ui_helpers.print_weather(weather_data_list)


def fetch_forecast(settings):
    """Fetch 5 day, 3 hour forecast from OpeWeatherMap based on zip code"""
    forecast_address = f"https://api.openweathermap.org/data/2.5/forecast?zip={settings["zip_code"]},us&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(forecast_address)
    verified = helpers.verify_response(r.status_code)
    if verified:
        forecast_dict = r.json()
        weather_data_list = forecast_dict['list']
        initial_size = len(weather_data_list)
        prompt = "Do you want to select a particular date?"
        prompt += "\nEnter 'y' for yes, anything else to print all forecast data: "
        helpers.refine_date(weather_data_list, prompt)
        ui_helpers.print_weather(weather_data_list)


def weather_by_city(settings):
    """Attempt to get the weather of a particular city entered by the user"""
    city = input("Enter city name: ").strip().title()

    city_list = helpers.same_name_cities(city)
    print(city_list)
    
    city_choice_dict = None
    if len(city_list) > 1:
        city_choice_dict = helpers.verify_city_choice(city_list)

    #print(city)
    city_address = f"https://api.openweathermap.org/data/2.5/weather?q={city}"
    if city_choice_dict:
        if city_choice_dict.get("state"):
            city_address += f",{city_choice_dict["state"]}"
        city_address += f",{city_choice_dict["country"]}"
    city_address += f"&appid={settings["API_KEY"]}&units=imperial"
    r = requests.get(city_address)
    verified = helpers.verify_response(r.status_code)
    if verified:
        city_dict = r.json()
        #print(city_dict)
        weather_data_list = [city_dict]
        ui_helpers.print_weather(weather_data_list) 
