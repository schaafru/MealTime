import pandas as pd
import socket
import pickle

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


def ingredients_getter():
    """
    receives ingredients and allergy information from main.py
    :return: a list of ingredients and allergy information from user for recipe_returner to access
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr} to main.py")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data = pickle.loads(data)
                print(f"data received from main.py: {data}")
                return data


def recipe_returner(ingredients, allergies):
    """
    :param ingredients: string from user input
    :param allergies: string for user input
    :return: a dictionary of recipe information as [name: , ingredients: , directions: ]
    """

    recipe = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        df = pd.read_excel('recipes_test.xlsx')
        row = 0
        for j in df.Ingredients:
            ingredient_match = 0
            if len(allergies) != 0:
                check = all(item in j.split() for item in allergies.split())
                if check:
                    row += 1
                    continue
            else:
                for i in ingredients.split():
                    words = j.split()
                    for k in words:
                        if i in k:
                            ingredient_match += 1
                    if ingredient_match == len(ingredients.split()):
                        recipe = {'name': str(df.iloc[row]['Title']), 'ingredients': str(df.iloc[row]['Ingredients']),
                                  'directions': str(df.iloc[row]['Directions'])}
                row += 1
        if recipe == "":
            print("No recipe found for ingredients and allergies given")
        else:
            print(f"data being sent back to main.py: {recipe}")
            send = pickle.dumps(recipe)
            s.sendall(send)
            data = s.recv(4096)


info = ingredients_getter()
ingredients = info[0]
allergies = info[1]
recipe_returner(ingredients, allergies)
