import pandas as pd


def recipe_finder(ingredients, allergies, fav_foods, user):
    df = pd.read_excel('recipes.xlsx')
    row = 0
    for j in df.Ingredients:
        check = all(item in j.split() for item in allergies)
        if check:
            row += 1
            print(f"this is the check: {check}")
            print(row)
            continue
        for i in ingredients:
            ingredient_match = 0
            words = j.split()
            for k in words:
                if i == k:
                    # print(f"match! i:{i} j:{k}")
                    ingredient_match += 1
            if ingredient_match == len(ingredients):
                with open(f'{user}_saved_recipe_name.txt', 'w') as f:
                    f.write(f"{str(df.iloc[row]['Name'])}\n")
                    f.close()
                with open(f'{user}_saved_recipe_ingredients.txt', 'w') as f:
                    f.write(f"{str(df.iloc[row]['Ingredients'])}\n")
                    f.close()
                with open(f'{user}_saved_recipe_instructions.txt', 'w') as f:
                    f.write(f"{str(df.iloc[row]['Directions'])}\n")
                    f.close()
                return True
        row += 1
    return False


# recipe_finder(['beef'], ['pork'], [''], "test")