import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os

from Database.db import SessionLocal, init_db
from sqlalchemy import exists
from Database.Models.menu import Dessert, Drink, Pizza
from Database.Models.ingredients import Ingredient
from Database.Models.delivery import DeliveryPerson, PostalCodeArea
from Database.Models.customer import Customer, CustomerAccount
import subprocess

# Initialize the database (create tables if not exists)
init_db()

def add_items_to_db(session, model, items):
    """
    Add a list of items to the database if they don't already exist.
    """
    try:
        # Just try to add each item and commit
        for item in items:
            session.add(item)

        session.commit()  # Commit once after processing all items
        print(f"{model.__name__} items added to the database!")

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
postal_code_areas = [
    PostalCodeArea(postal_code='11111', city='Maastricht', delivery_person_count=2),
    PostalCodeArea(postal_code='22222', city='Amsterdam', delivery_person_count=2),
    PostalCodeArea(postal_code='33333', city='Eindhoven', delivery_person_count=2),
    PostalCodeArea(postal_code='44444', city='Rotterdam', delivery_person_count=2),
    PostalCodeArea(postal_code='55555', city='Utrecht', delivery_person_count=2)
]

delivery_persons = [
    # Postal code area 1
    DeliveryPerson(first_name='John', last_name='Doe', postal_code_area_id=1),
    DeliveryPerson(first_name='Jane', last_name='Smith', postal_code_area_id=1),
    DeliveryPerson(first_name='Michael', last_name='Davis', postal_code_area_id=1),

    # Postal code area 2
    DeliveryPerson(first_name='Mike', last_name='Johnson', postal_code_area_id=2),
    DeliveryPerson(first_name='Sara', last_name='Brown', postal_code_area_id=2),
    DeliveryPerson(first_name='Laura', last_name='Green', postal_code_area_id=2),

    # Postal code area 3
    DeliveryPerson(first_name='Tom', last_name='Clark', postal_code_area_id=3),
    DeliveryPerson(first_name='Emily', last_name='White', postal_code_area_id=3),
    DeliveryPerson(first_name='Kevin', last_name='Adams', postal_code_area_id=3),

    # Postal code area 4
    DeliveryPerson(first_name='Alex', last_name='Taylor', postal_code_area_id=4),
    DeliveryPerson(first_name='Sophia', last_name='Lewis', postal_code_area_id=4),
    DeliveryPerson(first_name='Rachel', last_name='Wright', postal_code_area_id=4),

    # Postal code area 5
    DeliveryPerson(first_name='Chris', last_name='Walker', postal_code_area_id=5),
    DeliveryPerson(first_name='Anna', last_name='Hall', postal_code_area_id=5),
    DeliveryPerson(first_name='Luke', last_name='King', postal_code_area_id=5)
]



with SessionLocal() as session:
    add_items_to_db(session, Dessert, desserts)
    add_items_to_db(session, Drink, drinks)
    add_items_to_db(session, Pizza, pizzas)
    add_items_to_db(session, Ingredient, ingredients)
    add_items_to_db(session, PostalCodeArea, postal_code_areas)
    add_items_to_db(session, DeliveryPerson, delivery_persons)

def add_admin():
    # Create an admin account
    with SessionLocal() as session:
        admin_customer = Customer(
            first_name="Admin",
            last_name="User",
            gender="F",
            birthdate="1970-01-01",
            phone_number='0000000000',
            address="Admin Address",
            postal_code="00000"
        )

        admin_account = CustomerAccount(
            username="admin",
            password="admin",
            customer=admin_customer,
            total_pizza_count=0,
            discount_pizza_count=0,
            is_admin=True
        )

        session.add(admin_account)
        session.commit()

add_admin()
# adding ingredients, prices and diets to pizzas
# subprocess.run(["python3", "add_pizza_ingredients.py"])

