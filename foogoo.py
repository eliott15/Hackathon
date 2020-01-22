import spoonacular as sp
import pandas as pd
from collections import defaultdict

ID = 0
MISSING = 3
VEGETARIAN, VEGAN, GLUTEN, DAIRY = 2, 3, 4, 5
FILTERS_DICT = {'vegetarian':VEGETARIAN,'vegan':VEGAN, 'gluten': GLUTEN, 'dairy':DAIRY}
DATA = ['id','recipe_name','nb_missed_ing','missed_ing','missing_prices',
        'total_missing', 'instructions', 'price_per_serving', 'vegetarian',
        'vegan', 'gluten_free', 'dairy_free']

foogoo = sp.API("18b4d68fbd11492f8ac5fd4c771d2b44")


def get_recipe(list_ing):
    """Takes a list of ingredients as inputs.
    Returns a list of recipe ids, recipe names, number of missing ingredients,
    and the missing ingredients.
    """
    response = foogoo.search_recipes_by_ingredients(list_ing)
    data = response.json()
    recipe_name = [data[i]["title"] for i in range(len(data))]
    recipe_id = [data[i]["id"] for i in range(len(data))]
    nb_missed_ing = [data[i]["missedIngredientCount"] for i in range(len(data))]
    missed_ing = [[el['name'] for el in data[i]['missedIngredients']] for i in range(len(data))]
    return list(zip(recipe_id, recipe_name, nb_missed_ing, missed_ing))


def get_missing_ing_price(missed_ing):
    """Takes a list of missing ingredients as input.
    Returns a list of missing ingredients joined with their price,
    and the sum of their prices.
    """
    response = foogoo.parse_ingredients("\n".join(missed_ing))
    data = response.json()
    price_ing = [data[i]["estimatedCost"]["value"] for i in range(len(data))]
    name_ing = [data[i]["name"] for i in range(len(data))]
    return (list(zip(name_ing, price_ing)), sum(price_ing))


def get_info_recipe(recipe_id, serving):
    """Takes a recipe id and the number of serving as inputs.
    Returns:
        - The instruction of the recipe
        - The price per serving
        - If the recipe is vegetarian
        - If the recipe is vegan
        - If the recipe is gluten free
        - If the recipe is dairy free
    """
    response = foogoo.get_recipe_information_bulk(recipe_id, serving)
    data = response.json()
    d = data[0]
    instructions = d['instructions']
    price_per_serving = d['pricePerServing']
    vegetarian, vegan, gluten, dairy = d['vegetarian'], d['vegan'], d['glutenFree'], d['dairyFree']
    return instructions, price_per_serving, vegetarian, vegan, gluten, dairy


def select_recipe(ingredients, serving=2, filters=None):
    """Takes a list of ingredients, number of people to serve
    and a list of filters (among vegan, vegetarian, gluten free, dairy free).
    Returns a list of recipes corresponding to the given filters.
    """
    data_dict = defaultdict(list)
    recipes = get_recipe(ingredients)
    if not filters:
        for recipe in recipes:
            recipe_id = recipe[ID]
            missed_ing = recipe[MISSING]
            infos = get_info_recipe(recipe_id, serving)
            missing = get_missing_ing_price(missed_ing)
            tmp_data = list(recipe) + list(missing) + list(infos)
            for i, col in enumerate(DATA):
                data_dict[col].append(tmp_data[i])
    else:
        for recipe in recipes:
            recipe_id = recipe[ID]
            missed_ing = recipe[MISSING]
            infos = get_info_recipe(recipe_id, serving)
            flag = True
            for f in filters:
                flag *= infos[FILTERS_DICT[f]]
            if flag:
                missing = get_missing_ing_price(missed_ing)
            tmp_data = list(recipe) + list(missing) + list(infos)
            for i, col in enumerate(DATA):
                data_dict[col].append(tmp_data[i])
    return data_dict


def main():
    my_ingredients = ['tomato', 'pasta']
    my_recipes = select_recipe(my_ingredients)
    df = pd.DataFrame.from_dict(my_recipes)
    df.to_csv('recipes.csv')


if __name__ == '__main__':
    main()