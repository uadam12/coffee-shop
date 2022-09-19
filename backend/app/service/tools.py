from json import dumps
from flask import abort
from ..model import Drink


def not_null(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)

        if not value:
            abort(404, 'Drink(s) not found')

        return value

    return wrapper


def check(title):
    drink = Drink.query.filter_by(title=title).first()

    if drink is not None:
        abort(409, f'Drink {title} already exists.')


def get_recipe(recipes):
    if type(recipes) == dict:
        recipes = [recipes]

    for recipe in recipes:
        if type(recipe) != dict \
                or 'color' not in recipe \
                or 'parts' not in recipe:
            abort(400, 'Recipe must be dictionary or list of dictionaries with color and parts keys.')

    return dumps(recipes)
