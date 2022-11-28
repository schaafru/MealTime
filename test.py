import pandas as pd

df = pd.read_excel('test.xlsx')

row = 0
count = 1
for ingredient in df.Ingredients:
    if "chicken" in ingredient.split():
        ingredients = df.iloc[row]['Ingredients']
        break


for i in ingredients.split("@"):
    if i[0] == "[":
        i = i[1:]
    length = len(i) - 1
    if i[length] == "]":
        i = i[:-1]
    print(i)