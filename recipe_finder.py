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
            # print(f"Connected by {addr}")
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                data = pickle.loads(data)
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
        df = pd.read_excel('recipes.xlsx')
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
                    # print(i)
                    words = j.split()
                    for k in words:
                        # print(k)

                        ####COULD NOT A WRONG FIX#####
                        if i in k:
                            # print(f"match! i:{i} j:{k}")
                            ingredient_match += 1
                    # print(f"ingredient_match: {ingredient_match}")
                    # print(f"len(ingredients): {len(ingredients.split())}")
                    if ingredient_match == len(ingredients.split()):
                        recipe = {'name': str(df.iloc[row]['Name']), 'ingredients': str(df.iloc[row]['Ingredients']),
                                  'directions': str(df.iloc[row]['Directions'])}
                        # print(f"this is the send from recipe finder: {recipe}")
                row += 1
        send = pickle.dumps(recipe)
        s.sendall(send)
        data = s.recv(4096)


info = ingredients_getter()
# print(f"info: {info}")
ingredients = info[0]
# print(f"ingredients: {ingredients}")
allergies = info[1]
# print(f"allergies: {allergies}")
recipe_returner(ingredients, allergies)
