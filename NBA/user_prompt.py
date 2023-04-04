import visualize
import os


def prompt():
    plots = visualize.return_plots()
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Welcome! This is a showcase of how the NBA changed over time based on a 5 year timeframe.")
    invalid = False
    while True:
        
        if invalid:
            print("Invalid input, try again.")
            invalid = False
            
        print()
        print("Use 1-Q the characters on the left side to select between the options.")
        print("1. The change in points overtime;")
        print("2. Shot makes and attempts charts(3PT, FT, FG);")
        print("3. 3 Point shot attempt prevalence;")
        print("4. Field goal percentage(3PT, FT, FG, EFG);")
        print("5. Turnover to assist per pace relationship;")
        print("6. Offensive rebound impact;")
        print("7. Offensive rating and how turnovers and pace impacts it;")
        print("8. Defensive stats;")
        print("9. Weight and height relationship;")
        print("10. Save plots")
        print("11. Quit;")
        user_input = input("How would you like to proceed?: ")
        
        if user_input in plots:
            plots[user_input]()
        elif user_input == "11":
            break
        elif user_input.lower() == "10":
            save_prompt(plots)
        else:
            invalid = True
        
def save_prompt(plots):
    invalid = False
    while True:
        
        if invalid:
            print("Invalid input, try again.")
            invalid = False
            
        print()  
        print("Use 1-Q the characters on the left side to select between the options.")
        print("1. Save the change in points overtime;")
        print("2. Save shot makes and attempts charts(3PT, FT, FG);")
        print("3. Save 3 point shot attempt prevalence;")
        print("4. Save field goal percentage(3PT, FT, FG, EFG);")
        print("5. Save turnover to assist per pace relationship;")
        print("6. Save offensive rebound impact;")
        print("7. Save offensive rating relationship between turnovers and pace;")
        print("8. Save defensive stats;")
        print("9. Save weight and height relationship;")
        print("10. Save all the plots")
        print("11. Go back;")
        user_input = input("Enter your choice: ")
        
        if user_input in plots:
            plots[user_input](True)
        elif user_input == "11":
            break
        elif user_input == "10":
            for plot_call in plots.values():
                plot_call(True)
        else:
            invalid = True
        os.system('cls' if os.name == 'nt' else 'clear')
