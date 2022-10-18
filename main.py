import keyring
import pandas as pd


service_id = "MealTime"
username_key = "key"


def main():
    """
    Main function for running MealTime
    """
    welcome()


def welcome():
    print("\n")
    print("--------------------------------------------------------------------------")
    print("|                     Thank you for using MealTime!                      |")
    print("|          The one stop shop for all your recipe finding needs           |")
    print("--------------------------------------------------------------------------\n")
    print("1. Login")
    print("2. Create Account")
    print("3. Exit\n")

    while True:
        option = int(input())
        match option:
            case 1:
                login(1)
            case 2:
                create_account()
            case 3:
                print("Goodbye")
                exit(0)
            case _:
                print("Command not recognized. Try again")


def login(ease_of_use):
    print("\n")
    print("-----------------")
    print("|     LOGIN     |")
    print("-----------------\n")

    while True:
        if ease_of_use == 1:
            option = 1
        else:
            print("1. Login")
            print("2. Exit\n")

            option = int(input())
        match option:
            case 1:
                print("enter username: ")
                username = str(input())
                print("enter password: ")
                password = str(input())

                if username == keyring.get_password("MealTime", "key"):
                    if password == keyring.get_password("MealTime", username):
                        home(username)
                    else:
                        print(f"Incorrect password for {username}. Try again\n")
                else:
                    print("\nusername not found\n")
                    print("1. Try again")
                    print("2. Create account")
                    print("3. Exit\n")
                    option = int(input())

                    match option:
                        case 1:
                            continue
                        case 2:
                            create_account()
                        case 3:
                            exit(0)
                        case _:
                            print("Command not recognized. Try again")

            case 2:
                exit(0)
            case _:
                print("Command not recognized. Try again")


def create_account():
    print("\n")
    print("------------------")
    print("| CREATE ACCOUNT |")
    print("------------------\n")

    print("enter username: ")
    username = str(input())

    while True:
        print("enter password: ")
        pass1 = str(input())
        print("confirm password: ")
        pass2 = str(input())

        if pass1 == pass2:
            keyring.set_password("MealTime", username, pass1)
            keyring.set_password("MealTime", "key", username)
            print("Account created!\n")
            home(username)
        else:
            print("\nPasswords do not match. Try again\n")


def home(user):
    print("\n")
    print("------------------")
    print("|    MealTime    |")
    print("------------------")

    while True:
        print("\n1. Search for Recipes")
        print("2. View Profile")
        print("3. Logout\n")

        option = int(input())
        match option:
            case 1:
                recipe_search(user)
            case 2:
                profile(user)
            case 3:
                print("\nYou have been securely logged out\n")
                login(0)
            case _:
                print("\nCommand not recognized. Try again\n")


def recipe_search(user):
    print("\n")
    print("------------------")
    print("|  Recipe Finder |")
    print("------------------\n")
    print("The Recipe Finder finds a recipe within the database that contains every ingredient searched!")
    print("Enter list of ingredients separated by a space to search:")

    ingredients = str(input())
    ingredients = ingredients.split()
    df = pd.read_excel('recipes.xlsx')

    with open(f'{user}_allergies.txt', 'r+') as f:
        allergies = f.read()
        allergies = allergies.split()
        f.close()
    with open(f'{user}_fav_foods.txt', 'r+') as f:
        fav_foods = f.read()
        fav_foods = fav_foods.split()
        f.close()

    row = 0
    for i in df.Ingredients:
        check = check = all(item in i for item in allergies)
        if check:
            continue
        count = len(ingredients)
        counter = 0
        for j in ingredients:
            if j in i:
                counter += 1
        if counter == count:
            print(f"\nrecipe for '{df.iloc[row]['Name']}' found!\n")
            print("1. View Recipe")
            print("2. Save Recipe")
            print("3. Back")
            print("4. Return To Home\n")

            option = int(input())
            match option:
                case 1:
                    print(f"Name: {str(df.iloc[row]['Name'])}")
                    print(f"Ingredients: {str(df.iloc[row]['Ingredients'])}")
                    print(f"Directions: {str(df.iloc[row]['Directions'])}")
                    while True:
                        print("\n1. Save Recipe")
                        print("2. Back To Home\n")
                        option = int(input())

                        match option:
                            case 1:
                                print(f"\n'{str(df.iloc[row]['Name'])}' has been added to Saved Recipes!")
                                with open(f'{user}_saved_recipes.txt', 'w') as f:
                                    f.write(f"Name: {str(df.iloc[row]['Name'])}\n")
                                    f.write(f"Ingredients: {str(df.iloc[row]['Ingredients'])}\n")
                                    f.write(f"Directions: {str(df.iloc[row]['Directions'])}\n")
                                    f.close()

                            case 2:
                                home(user)
                            case _:
                                print("\nCommand not recognized. Try again\n")
                case 2:
                    print(f"\n'{str(df.iloc[row]['Name'])}' has been added to Saved Recipes!")
                    with open(f'{user}_saved_recipes.txt', 'w') as f:
                        f.write(f"Name: {str(df.iloc[row]['Name'])}\n")
                        f.write(f"Ingredients: {str(df.iloc[row]['Ingredients'])}\n")
                        f.write(f"Directions: {str(df.iloc[row]['Directions'])}\n")
                        f.close()

                    while True:
                        print("\n1. Back To Home")
                        option = int(input())
                        match option:
                            case 1:
                                home(user)
                            case _:
                                print("\nCommand not recognized. Try again\n")
                case 3:
                    recipe_search(user)
                case 4:
                    home(user)
                case _:
                    print("\nCommand not recognized. Try again\n")
        row += 1
    print("\nNo recipes found!")

    # print(f"ingredients: {ingredients}. allergies: {allergies}. favorite foods: {fav_foods}\n")


def recipe_view():
    pass


def profile(user):
    print("\n")
    print("------------------")
    print("|     Profile    |")
    print("------------------")
    try:
        with open(f'{user}_allergies.txt', 'r+') as f:
            allergies = f.read()
            f.close()
        with open(f'{user}_fav_foods.txt', 'r+') as f:
            fav_foods = f.read()
            f.close()
    except Exception:
        allergies = None
        fav_foods = None
    print(f"Username: {user}")
    print(f"Current Allergies: {allergies}")
    print(f"Favorite Food(s): {fav_foods}")

    while True:
        print("\n1. View Saved Recipes")
        print("2. Edit Preferences")
        print("3. Return To Home")
        print("4. Logout\n")

        option = int(input())
        match option:
            case 1:
                saved_recipes(user)
            case 2:
                preferences(user)
            case 3:
                home(user)
            case 4:
                print("You have been securely logged out")
                login(0)
            case _:
                print("Command not recognized. Try again")


def saved_recipes(user):
    try:
        with open(f'{user}_saved_recipes.txt', 'r') as f:
            print(f.readlines())
    except:
        print("\nNo saved recipes!")


def preferences(user):
    print("\n")
    print("------------------")
    print("|   Preferences  |")
    print("------------------\n")

    while True:
        print("1. Enter Allergies")
        print("2. Enter Favorite Foods")
        print("3. Return To Profile\n")

        option = int(input())
        match option:
            case 1:
                with open(f'{user}_allergies.txt', 'w') as f:
                    print("\nAdding allergies will cause recipes containing those ingredients to not appear in a search!\n")
                    print("\nEnter allergies separated by a space: ")
                    allergies = str(input())
                    f.write(allergies)
                    f.close()
            case 2:
                with open(f'{user}_fav_foods.txt', 'w') as f:
                    print("\nAdding favorite foods will make those recipes more likely to appear in a search!\n")
                    print("\nEnter favorite foods separated by a space: ")
                    fav_foods = str(input())
                    f.write(fav_foods)
                    f.close()
            case 3:
                profile(user)
            case _:
                print("Command not recognized. Try again")


if __name__ == "__main__":
    main()
