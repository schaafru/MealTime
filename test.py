import pandas as pd


list = ['beef', 'pork']
# list.append("milk")
# print(list)

df = pd.read_excel('recipes.xlsx')

print(df.iloc[1]['Name'])
print(df.iloc[1]['Ingredients'])
print(df.iloc[1]['Directions'])
