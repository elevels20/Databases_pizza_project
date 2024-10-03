from Database.db import SessionLocal, init_db
from sqlalchemy import exists
from Database.Models.menu import Dessert, Drink, Pizza
from Database.Models.ingredients import Ingredient
import subprocess

 # Initialize the database (create tables if not exists)
init_db()

def add_items_to_db(session, model, items):
    """
    Add a list of items to the database if they don't already exist.
    """
    try:
        # Iterate through the list of items
        for item in items:
            # Check if the item already exists based on the name
            item_exists = session.query(exists().where(model.name == item.name)).scalar()

            if not item_exists:
                session.add(item)
            else:
                print(f"{item.name} already exists in the database.")

        session.commit()  # Commit once after processing all items
        print(f"{model.__name__} addition process completed!")

    except Exception as e:
        session.rollback()  # Rollback if any error occurs
        print(f"Error adding {model.__name__}: {e}")
    finally:
        session.close()

desserts = [
    Dessert(name='Ice Cream', price=4.0, diet="Vegetarian"),
    Dessert(name='Cheesecake', price=5.5, diet="Vegetarian"),
    Dessert(name='Brownie', price=3.0, diet="Vegetarian"),
    Dessert(name='Apple Pie', price=4.5, diet="Vegetarian"),
    Dessert(name='Tiramisu', price=6.0, diet="Vegetarian")
]

drinks = [
    Drink(name='Coca Cola', price=2.5),
    Drink(name='Sprite', price=2.5),
    Drink(name='Fanta', price=2.5),
    Drink(name='Water', price=1.5),
    Drink(name='Orange Juice', price=3.0)
]

pizzas = [
    Pizza(name='Margherita', price=0.0),
    Pizza(name='Pepperoni', price=0.0),
    Pizza(name='Hawaii', price=0.0),
    Pizza(name='Four cheese', price=0.0),
    Pizza(name='BBQ chicken', price=0.0),
    Pizza(name='Veggie', price=0.0),
    Pizza(name='Ham', price=0.0),
    Pizza(name='Meatlovers', price=0.0),
    Pizza(name='Spinach feta', price=0.0),
    Pizza(name='Ham mushroom', price=0.0)
]

ingredients = [
    Ingredient(name='Tomato Sauce', price=0.5, diet='Vegan'),
    Ingredient(name='Mozzarella', price=1.0, diet='Vegetarian'),
    Ingredient(name='Pepperoni', price=1.5),
    Ingredient(name='Ham', price=1.5),
    Ingredient(name='Pineapple', price=1.0, diet='Vegan'),
    Ingredient(name='Bell Peppers', price=0.8, diet='Vegan'),
    Ingredient(name='Onions', price=0.5, diet='Vegan'),
    Ingredient(name='Mushrooms', price=1.0, diet='Vegan'),
    Ingredient(name='Olives', price=1.0, diet='Vegan'),
    Ingredient(name='Spinach', price=0.8, diet='Vegan'),
    Ingredient(name='Chicken', price=2.0),
    Ingredient(name='BBQ Sauce', price=1.0, diet='Vegan'),
    Ingredient(name='Cheddar', price=1.2, diet='Vegetarian'),
    Ingredient(name='Parmesan', price=1.5, diet='Vegetarian'),
    Ingredient(name='Feta', price=1.5, diet='Vegetarian'),
    Ingredient(name='Olive Oil', price=0.5, diet='Vegan'),
    Ingredient(name='Garlic', price=0.5, diet='Vegan')
]


with SessionLocal() as session:
    add_items_to_db(session, Dessert, desserts)
    add_items_to_db(session, Drink, drinks)
    add_items_to_db(session, Pizza, pizzas)
    add_items_to_db(session, Ingredient, ingredients)

# adding ingredients, prices and diets to pizzas
subprocess.run(["python3", "add_pizza_ingredients.py"])

