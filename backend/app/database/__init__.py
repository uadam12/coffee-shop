from os import path
from secrets import token_hex as key

base = path.abspath(path.dirname(__file__))
db_file = path.join(base, 'CoffeeShop.db')


class Config(object):
    SECRET_KEY = key(32)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_file}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
