import keyring
import socket
import pickle


service_id = "MealTime"
username_key = "key"
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def main():
    """
    Main function for running MealTime
    """
    welcome()


def welcome():
    print("\n")
    print(".___  ___.  _______     ___       __      .___________. __  .___  ___.  _______")
    print("|   \/   | |   ____|   /   \     |  |     |           ||  | |   \/   | |   ____|")
    print("|  \  /  | |  |__     /  ^  \    |  |     `---|  |----`|  | |  \  /  | |  |__")
    print("|  |\/|  | |   __|   /  /_\  \   |  |         |  |     |  | |  |\/|  | |   __|")
    print("|  |  |  | |  |____ /  _____  \  |  `----.    |  |     |  | |  |  |  | |  |____")
    print("|__|  |__| |_______/__/     \__\ |_______|    |__|     |__| |__|  |__| |_______|")
    print("   --------------------------------------------------------------------------")
    print("   |                     Thank you for using MealTime!                      |")
    print("   |          The one stop shop for all your recipe finding needs           |")
    print("   --------------------------------------------------------------------------\n")
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
    print(".___  ___.  _______     ___       __      .___________. __  .___  ___.  _______")
    print("|   \/   | |   ____|   /   \     |  |     |           ||  | |   \/   | |   ____|")
    print("|  \  /  | |  |__     /  ^  \    |  |     `---|  |----`|  | |  \  /  | |  |__")
    print("|  |\/|  | |   __|   /  /_\  \   |  |         |  |     |  | |  |\/|  | |   __|")
    print("|  |  |  | |  |____ /  _____  \  |  `----.    |  |     |  | |  |  |  | |  |____")
    print("|__|  |__| |_______/__/     \__\ |_______|    |__|     |__| |__|  |__| |_______|\n")

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


def information_send(info):
    """
    sends list of ingredients and allergy information using socket to microservice
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send = pickle.dumps(info)
        s.sendall(send)
        data = s.recv(4096)


def recipe_receive():
    """
    receives dictionary from socket containing all information on recipe
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT + 1))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data = pickle.loads(data)
                return data


def display_directions(results):
    """
    prettifies the directions from results passed to the function and displays to user
    :param results: dictionary of information for a recipe
    :return: None
    """
    directions = results['directions']
    print(f"The directions for {results['name']} are:\n")
    for i in directions.split("."):
        print(i)


def display_ingredients(results):
    """
    prettifies the ingredient list from results passed to the function and displays to user
    :param results: dictionary of information for a recipe
    :return: None
    """
    ingredients = results['ingredients']
    print(f"The ingredients you will need for {results['name']} are:\n")
    for i in ingredients.split("@"):
        if i[0] == "[":
            i = " " + i[1:]
        length = len(i) - 1
        if i[length] == "]":
            i = i[:-1]
        print(f"   {i}")


def recipe_search(user):
    print("\n")
    print("------------------")
    print("|  Recipe Finder |")
    print("------------------\n")
    print("Enter list of ingredients separated by a space to search:\n")

    try:
        with open(f'users/{user}_allergies.txt', 'r+') as f:
            allergies = f.read()
            f.close()
    except Exception:
        allergies = ""

    try:
        with open(f'users/{user}_pantry.txt', 'r+') as f:
            pantry_items = f.read()
            f.close()
    except Exception:
        pantry_items = ""

    ingredients = input()
    ingredients = ingredients + " " + pantry_items
    info = ingredients, allergies
    information_send(info)
    results = recipe_receive()

    if bool(results):
        # results = [name: x, ingredients: y, directions: z]
        # if a recipe was found, function will return True
        print("\nRecipe for '" + results['name'] + "' found!")
        while True:
            print("\n1. View Directions")
            print("2. View Ingredients")
            print("3. Save Recipe")
            print("4. Return To Home\n")

            option = int(input())
            match option:
                case 1:
                    display_directions(results)
                case 2:
                    display_ingredients(results)
                case 3:
                    save_to_recipes(user, results)
                case 4:
                    home(user)
                case _:
                    print("Command not recognized. Try again")

    else:
        # if a recipe wasn't found
        print("\nNo recipe found!\n")
        print("1. Search using different ingredients")
        print("2. Return to Home")

        option = int(input())
        match option:
            case 1:
                recipe_search(user)
            case 2:
                home(user)
            case _:
                print("Command not recognized. Try again")


def pantry(user):
    print("\n")
    print("------------------")
    print("|     Pantry     |")
    print("------------------\n")
    print("Your current pantry items are: ")

    try:
        with open(f'users/{user}_pantry.txt', 'r') as f:
            pantry_items = f.read()
            f.close()
    except Exception:
        pantry_items = ""

    if not pantry_items:
        print("empty pantry")

    else:
        print(pantry_items)

    while True:
        print("\n1. Update Pantry Items")
        print("2. Return To Profile")

        option = int(input())
        match option:
            case 1:
                print("Enter your pantry items:")
                pantry_items = input()
                with open(f'users/{user}_pantry.txt', 'w') as f:
                    f.write(pantry_items)
                    f.close()
                pantry(user)
            case 2:
                profile(user)
            case _:
                print("Command not recognized. Try again")


def profile(user):
    print("\n")
    print("------------------")
    print("|     Profile    |")
    print("------------------")
    try:
        with open(f'users/{user}_allergies.txt', 'r') as f:
            allergies = f.read()
            f.close()
    except Exception:
        allergies = ""

    fav_foods = ""
    print(f"Username: {user}")
    print(f"Current Allergies: {allergies}")
    print(f"Favorite Food(s): {fav_foods}")

    while True:
        print("\n1. View Saved Recipes")
        print("2. Update Pantry")
        print("3. Edit Preferences")
        print("4. Return To Home")
        print("5. Logout\n")

        option = int(input())
        match option:
            case 1:
                view_saved_recipes(user)
                home(user)
            case 2:
                pantry(user)
            case 3:
                preferences(user)
            case 4:
                home(user)
            case 5:
                print("You have been securely logged out")
                login(0)
            case _:
                print("Command not recognized. Try again")


def save_to_recipes(user, recipe):
    """

    :param user: username of current login
    :param recipe: dictionary of recipe last viewed in format [name: x, ingredients: y, directions: z]
    :return: None
    """
    print(f"\n'{recipe['name']}' saved to recipes!")
    with open(f'users/{user}_saved_recipes.txt', 'w') as f:
        f.write(f"{recipe}")
        f.close()


def view_saved_recipes(user):
    try:
        with open(f'users/{user}_saved_recipes.txt', 'r') as f:
            print(f.readlines())
    except Exception:
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
                with open(f'users/{user}_allergies.txt', 'w') as f:
                    print("\nAdding allergies will cause recipes containing those ingredients to not appear in a "
                          "search!\n")
                    print("\nEnter allergies separated by a space: ")
                    allergies = str(input())
                    f.write(allergies)
                    f.close()
            case 2:
                with open(f'users/{user}_fav_foods.txt', 'w') as f:
                    print("\nAdvanced option: Adding favorite foods will make those recipes more likely to appear in"
                          " a search! Editing this may lead to undesirable results!\n")
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
