from foogoo import *
from date_recognizer import *
from datetime import datetime


def get_ingredients(ingredients_df):
    """Takes as input a dataframe of ingredients with their information (name, expiry date, picture, diet).
    Returns a list of ingredients names and expiry dates.
    """
    ing_list = []
    for i in range(len(ingredients_df)):
        infos = ingredients_df.iloc[i, :]
        name, date, picture = infos[0], infos[1], infos[2]
        if date:
            ing_list.append((name, date))
        else:
            if picture:
                pic_date = find_date(picture)
                ing_list.append((name, pic_date))

    return ing_list


def optimize_fridge(ingredient_infos, nb_ing=2):
    """Takes as input a list of ingredients with their information (name, expiry date) and an int nb_ing.
    Returns a list of at most nb_ing ingredients names to use.
    """
    li = ingredient_infos
    ordered_list = sorted(list(filter(lambda x: x[1], li)), key=lambda x: datetime.strptime(x[1], '%d/%m/%Y'),
                          reverse=False)
    ingredients = [ordered_list[i][0] for i in range(nb_ing)]
    return ingredients


def propose_recipes(ingredients_df):
    """Takes as input a dataframe of ingredients with their information (name, expiry date, picture, diet).
    Returns a dataframe of recipes.
    """
    diet = ingredients_df.iloc[0, -1]
    ingredients_info = get_ingredients(ingredients_df)
    ingredients = optimize_fridge(ingredients_info)
    if diet == 'None':
        my_recipes = select_recipe(ingredients)
    else:
        my_recipes = select_recipe(ingredients, filters=[diet])
    df = pd.DataFrame.from_dict(my_recipes)
    df.to_csv('static/data/recipes.csv')
    return df


def combine_recipes(recipe_list):
    """Takes a list of recipes and the dataframe of recipes as inputs.
    Returns the list of missing ingredients, and the corresponding prices.
    """
    df = pd.read_csv("static/data/recipes.csv")
    missing_ingredients = []
    missing_price = []
    for recipe in recipe_list:
        ings = df[df['recipe_name'] == recipe]['missing_prices']
        for ing in ings:
            missing_ingredients.append(ing[0])
            missing_price.append(ing[1])
    return missing_ingredients, missing_price
