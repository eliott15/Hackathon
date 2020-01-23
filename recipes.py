import json


def read_recipes(json_file):
    """Takes a json file name as input.
    Returns the dictionary of contained data.
    """
    with open(json_file, 'r') as f:
        dictionary = json.load(f)
    return dictionary


def get_recipe_ingredients(dictionary):
    """Takes the recipes dictionary as input.
    Returns a list of recipes in the format (key (string), ingredients (list)).
    """
    ingredients = []
    for i, el in enumerate(dictionary):
        try:
            ing = dictionary[el]['ingredients']
            if len(ing) > 1:
                ingredients.append((el, ing))
            elif len(ing) == 1:
                ingredients.append((el, ing[0].split(',')))
        except KeyError:
            pass
    return ingredients


def get_price(ingredient):
    return''


def get_nutritional_info(ingredient):
    return''


def get_recipes(ingredients, recipes_list):
    """Takes a list of available ingredients and list of recipes as inputs.
    Each recipe msut be in the format (key (string), ingredients (list)).
    Returns a sub-list of recipes that contain only available ingredients.
    """
    possible_recipes = []
    for recipe in recipes_list:
        recipe_ingredients = recipe[1]
        flag = True
        i = 0
        while flag and i < len(recipe_ingredients):
            tmp = 0
            r_ing = recipe_ingredients[i]
            for ing in ingredients:
                if ing in r_ing.replace(',', '').split():
                    tmp += 1
            flag = (tmp > 0)
            i += 1
        if flag:
            possible_recipes.append(recipe[0])
    return possible_recipes


def get_recipes_names(dictionary, recipes_keys):
    """Returns the titles of recipes given recipes keys."""
    names = []
    for key in recipes_keys:
        names.append(dictionary[key]['title'])
    return names


def main():
    json_file = "recipes_raw_nosource_fn.json"
    data_dictionary = read_recipes(json_file)
    recipes_list = get_recipe_ingredients(data_dictionary)
    my_ingredients = ['salt', 'milk', 'pistachio', 'butter', 'celery',
                      'pepper', 'onions', 'parsley', 'crabmeat', 'cracker',
                      'mustard', 'Dash', 'cream', 'crabmeat']
    my_recipes = get_recipes(my_ingredients, recipes_list)
    my_recipes_titles = get_recipes_names(data_dictionary, my_recipes)
    print('\n'.join(my_recipes_titles))


if __name__ == '__main__':
    main()