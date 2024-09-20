from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database import engine
from tables.ingredient import Ingredient

Session = sessionmaker(bind=engine)
session = Session()


ingredients = [
    Ingredient(name='Mozzarella', price=1.0, diet='vegetarian'),
    Ingredient(name='Cheddar', price=1.2, diet='vegetarian'),
    Ingredient(name='Parmesan', price=1.5, diet='vegetarian'),
    Ingredient(name='Gorgonzola', price=1.7, diet='vegetarian'),
    Ingredient(name='Feta', price=1.5, diet='vegetarian'),
    Ingredient(name='Bell Peppers', price=0.8, diet='vegan'),
    Ingredient(name='Onions', price=0.5, diet='vegan'),
    Ingredient(name='Mushrooms', price=1.0, diet='vegan'),
    Ingredient(name='Olives', price=1.0, diet='vegan'),
    Ingredient(name='Spinach', price=0.8, diet='vegan'),
    Ingredient(name='Artichokes', price=1.5, diet='vegan'),
    Ingredient(name='Tomatoes', price=0.6, diet='vegan'),
    Ingredient(name='Chicken', price=2.0, diet=''),
    Ingredient(name='Ham', price=1.5, diet=''),
    Ingredient(name='Pepperoni', price=1.5, diet=''),
    Ingredient(name='Bacon', price=1.8, diet=''),
    Ingredient(name='Sausage', price=1.7, diet=''),
    Ingredient(name='Beef', price=2.0, diet=''),
    Ingredient(name='Salami', price=1.5, diet=''),
    Ingredient(name='Anchovies', price=1.2, diet=''),
    Ingredient(name='BBQ Sauce', price=1.0, diet='vegan'),
    Ingredient(name='Tomato Sauce', price=0.5, diet='vegan'),
    Ingredient(name='Pesto Sauce', price=1.0, diet='vegetarian'),
    Ingredient(name='Olive Oil', price=0.5, diet='vegan'),
    Ingredient(name='Garlic', price=0.5, diet='vegan'),
    Ingredient(name='Truffle Oil', price=1.8, diet='vegan'),
    Ingredient(name='Pineapple', price=1.0, diet='vegan'),
    Ingredient(name='Avocado', price=1.5, diet='vegan'),
    Ingredient(name='Sundried Tomatoes', price=1.2, diet='vegan'),
    Ingredient(name='Egg', price=0.7, diet='vegetarian')
]


for ingredient in ingredients:
    ingredient_exists = session.query(exists().where(Ingredient.name == ingredient.name)).scalar()
    if not ingredient_exists:
        session.add(ingredient)

    else:
        print(f"{ingredient.name} already exists in the database.")

session.commit()
session.close()

print("Ingredient addition process completed!")
