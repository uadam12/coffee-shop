from flask import Blueprint

from .. import service
from .tools import data, get_data
from .auth import requires_auth

bp = Blueprint('bp', __name__)


def restart_db():
    service.db_restart()

    for i in range(12):
        service.post_drink({
           'title': f'Water {i + 1}',
           'recipe': [{
                "name": "water",
                "color": "blue",
                "parts": 1
            }]
        })


@bp.route('/drinks')
def get_drinks_summary():
    summary = service.drinks_summary()
    return data(drinks=summary)


@bp.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    details = service.drinks_details()
    return data(drinks=details)


@bp.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    drink = service.create_drink(get_data())
    return data(drinks=[drink])


@bp.route('/drinks/<int:drink_id>', methods=['delete'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    service.delete_drink(drink_id)
    return data(delete=drink_id)


@bp.route('/drinks/<int:drink_id>', methods=['patch'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    drink = service.update_drink(drink_id, get_data())
    return data(drinks=[drink])
