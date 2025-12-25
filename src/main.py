import ui_helpers
import config
import fetch


def main():

    print("\nWelcome to CLI-Mate!" 
          "\nA simple weather fetching application written in Python")

    settings = config.load_settings()

    while True:
        ui_helpers.print_menu()
        choice = input("\nWhat would you like to to? ").strip()
        
        if choice == '1':
            ui_helpers.print_info()
        elif choice == '2':
            config.set_settings(settings)
        elif choice == '3':
            fetch.fetch_weather(settings)
        elif choice == '4':
            fetch.fetch_forecast(settings)
        elif choice == '5':
            fetch.weather_by_city(settings)
        elif choice == '6':
            break
        else:
            print("INVALID INPUT")
            
if __name__ == '__main__':
    main()
