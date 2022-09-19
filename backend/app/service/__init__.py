from .. import db
from ..model import Drink, save
from .tools import not_null, check, get_recipe


# RESTART
def db_restart():
    db.drop_all()
    db.create_all()


# CREATE
@save
def post_drink(data):
    title = data['title']
    
    check(title)

    new_drink = Drink(
        title=title,
        recipe=get_recipe(data['recipe'])
    )

    db.session.add(new_drink)


@not_null
def create_drink(data):
    post_drink(data)
    drink = Drink.query.order_by(Drink.id.desc()).first()
    return drink.long()


# READ
def get_drinks():
    return Drink.query.all()


@not_null
def get_drink(drink_id):
    return Drink.query.get(drink_id)


@not_null
def drinks_summary():
    return [drink.short() for drink in get_drinks()]


@not_null
def drinks_details():
    return [drink.long() for drink in get_drinks()]


# UPDATE
@save
def patch_drink(drink_id, data):
    drink = get_drink(drink_id)
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    if title is not None:
        check(title)
        drink.title = title

    if recipe is not None:
        drink.recipe = get_recipe(recipe)


@not_null
def update_drink(drink_id, data):
    patch_drink(drink_id, data)
    return get_drink(drink_id).long()


# DELETE
@save
def delete_drink(drink_id):
    drink = get_drink(drink_id)
    db.session.delete(drink)
