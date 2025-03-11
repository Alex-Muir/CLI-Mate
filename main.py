import helpers as h

def main():

    print("\nWelcome to CLI-Mate!" 
          "\nA simple weather fetching application written in Python")

    settings = h.load_settings()

    while True:
        h.print_menu()
        choice = input("\nWhat would you like to to? ")
        
        if choice == '1':
            h.print_info()
        elif choice == '2':
            h.set_settings(settings)
        elif choice == '3':
            h.fetch_weather(settings)
        elif choice == '4':
            h.fetch_forecast(settings)
        elif choice == '5':
            print(f"Choice: {choice}")
        elif choice == '6':
            break
        else:
            print("INVALID INPUT")
            
if __name__ == '__main__':
    main()
