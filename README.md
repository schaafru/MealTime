# MealTime

How to request data:
1. Start recipe_finder.py and main.py as two seperate processes
2. Within your main.py application, passing information to information_send() will open a socket connection between main.py and recipe_finder.py. This will
then request data from the microservice

How to recive data:
While recipe_finder.py and main.py are started in seperate processes:
1. Calling recipe_receive() in main.py will open a socket connection to recipe_finder.py and receive a recipe (if one was found)


![assignment8](https://user-images.githubusercontent.com/81342619/201745679-eca6a676-b245-4955-a9a1-f6b59a806987.png)
