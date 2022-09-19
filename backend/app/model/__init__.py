from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import json

db = SQLAlchemy()


def save(func):
    def wrapper(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return returned_value
    return wrapper


class Drink(db.Model):
    __tablename__ = 'drinks'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    recipe = Column(String(180), nullable=False)

    def short(self):
        recipes = json.loads(self.recipe)
        short_recipe = [{
            'color': recipe['color'], 
            'parts': recipe['parts']
        } for recipe in recipes]

        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def __repr__(self):
        return json.dumps(self.short())
