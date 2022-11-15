ingredients = "Combine the milk and breadcrumbs. Place the breadcrumbs in a small bowl, pour in the milk, and stir to combine. Set aside while preparing"
letters = len(ingredients)
remaining = len(ingredients)
start = 0
end = 100

if letters > 100:
    while remaining > 100:
        print(ingredients[start:end])
        start = end
        end += 100
        remaining -= 100
    print(ingredients[start:end])
