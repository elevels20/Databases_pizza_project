from Database.db import SessionLocal, init_db
from sqlalchemy.orm import Session
from sqlalchemy import exists
from Database.Models.menu import Pizza
from Database.Models.ingredients import Ingredient, PizzaIngredient
from typing import List, Tuple

# Initialize the database (create tables if not exists)
#init_db()

def add_calculatd_price(session: Session, pizza: Pizza) -> None:
    """
    Calculate the price of a pizza, calculated based on the sum of its ingredient costs, a 40% profit margin, and the inclusion of a 9% VAT.
    Add calculated price to table.
    """
    try:
        # Calculate the cost of the ingredients
        total_price = sum(ingredient.ingredient.price * ingredient.quantity for ingredient in pizza.pizza_ingredients)

        # Add a 40% profit margin
        total_price *= 1.40 

        # Add a 9% VAT
        total_price *= 1.09

        # Add rounded price to table
        pizza.price = round(total_price, 2)

        session.commit()
    
    except Exception as e:
        print(f"Error adding price to {pizza.name}: {e}")
    #finally:
    #    session.close()

def add_diet(session: Session, pizza: Pizza):
    """
    Determine if a pizza is vegan or vegetarian.
    Add this information to table.
    """
    try:
        if all(ingredient.ingredient.diet == "Vegan" for ingredient in pizza.pizza_ingredients):
            pizza.diet = "Vegan"
        elif all(ingredient.ingredient.diet in ["Vegan", "Vegetarian"] for ingredient in pizza.pizza_ingredients):
            pizza.diet = "Vegetarian"
        else:
            pizza.diet = None
        session.commit()
    except Exception as e:
        print(f"Error determining diet of {pizza.name}: {e}")
    #finally:
    #    session.close()

def add_ingredients_to_pizza(session: Session, pizza: Pizza, ingredients: List[Tuple[Ingredient, int]]) -> None:
    """
    Add ingredients to a given pizza if they are not already associated.
    """
    try:
        # Iterate through the list of ingredients
        for ingredient, quantity in ingredients:
            # Check if the ingredient is already added to the pizza
            pizza_ingredient_exists = session.query(PizzaIngredient).filter_by(
                pizza_id = pizza.pizza_id,
                ingredient_id = ingredient.ingredient_id
            ).first()

            # If not, add it to the pizza
            if not pizza_ingredient_exists:
                pizza_ingredient = PizzaIngredient(
                    pizza = pizza,
                    ingredient = ingredient,
                    quantity = quantity 
                )
                session.add(pizza_ingredient)
                print(f"Added {ingredient.name} to {pizza.name}")
            else:
                print(f"{ingredient.name} already added to {pizza.name}")
        session.commit()

    except Exception as e:
        print(f"Error adding ingredients to {pizza.name}: {e}")
    #finally:
    #    session.close()

with SessionLocal() as session: 
    pizzas = {
        'Margherita': session.query(Pizza).filter_by(name='Margherita').first(),
        'Pepperoni': session.query(Pizza).filter_by(name='Pepperoni').first(),
        'Hawaii': session.query(Pizza).filter_by(name='Hawaii').first(),
        'Veggie': session.query(Pizza).filter_by(name='Veggie').first(),
        'BBQ chicken': session.query(Pizza).filter_by(name='BBQ chicken').first(),
        'Ham': session.query(Pizza).filter_by(name='Ham').first(),
        'Four cheese': session.query(Pizza).filter_by(name='Four cheese').first(),
        'Spinach feta': session.query(Pizza).filter_by(name='Spinach feta').first(),
        'Meatlovers': session.query(Pizza).filter_by(name='Meatlovers').first(),
        'Ham mushroom': session.query(Pizza).filter_by(name='Ham mushroom').first(),
    }

    tomato_sauce = session.query(Ingredient).filter_by(name='Tomato Sauce').first()
    mozzarella = session.query(Ingredient).filter_by(name='Mozzarella').first()
    pepperoni = session.query(Ingredient).filter_by(name='Pepperoni').first()
    ham = session.query(Ingredient).filter_by(name='Ham').first()
    pineapple = session.query(Ingredient).filter_by(name='Pineapple').first()
    bell_peppers = session.query(Ingredient).filter_by(name='Bell Peppers').first()
    onions = session.query(Ingredient).filter_by(name='Onions').first()
    mushrooms = session.query(Ingredient).filter_by(name='Mushrooms').first()
    olives = session.query(Ingredient).filter_by(name='Olives').first()
    spinach = session.query(Ingredient).filter_by(name='Spinach').first()
    chicken = session.query(Ingredient).filter_by(name='Chicken').first()
    bbq_sauce = session.query(Ingredient).filter_by(name='BBQ Sauce').first()
    cheddar = session.query(Ingredient).filter_by(name='Cheddar').first()
    parmesan = session.query(Ingredient).filter_by(name='Parmesan').first()
    feta = session.query(Ingredient).filter_by(name='Feta').first()
    garlic = session.query(Ingredient).filter_by(name='Garlic').first()
    olive_oil = session.query(Ingredient).filter_by(name='Olive Oil').first()

    add_ingredients_to_pizza(session, pizzas['Margherita'], [
        (tomato_sauce, 1),
        (mozzarella, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Pepperoni'], [
        (tomato_sauce, 1),
        (mozzarella, 1),
        (pepperoni, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Hawaii'], [
        (tomato_sauce, 1),
        (mozzarella, 1),
        (ham, 1),
        (pineapple, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Veggie'], [
        (tomato_sauce, 1),
        #(mozzarella, 1),
        (bell_peppers, 1),
        (onions, 1),
        (mushrooms, 1),
        (olives, 1),
        (spinach, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['BBQ chicken'], [
        (bbq_sauce, 1),
        (mozzarella, 1),
        (chicken, 1),
        (onions, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Ham'], [
        (tomato_sauce, 1),
        (mozzarella, 1),
        (ham, 1),
    ])

    add_ingredients_to_pizza(session, pizzas['Four cheese'], [
        (tomato_sauce, 1),
        (mozzarella, 1),
        (cheddar, 1),
        (parmesan, 1),
        (feta, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Spinach feta'], [
        (tomato_sauce, 1),
        (spinach, 1),
        (feta, 1),
        (garlic, 1),
        (olive_oil, 1)
    ])

    add_ingredients_to_pizza(session, pizzas['Meatlovers'], [
        (bbq_sauce, 1),
        (mozzarella, 1),
        (ham, 1),
        (pepperoni, 1),
        (chicken, 1),
    ])

    add_ingredients_to_pizza(session, pizzas['Ham mushroom'], [
        (tomato_sauce, 1),
        (mozzarella, 1),
        (ham, 1),
        (mushrooms, 1),
    ])

    for pizza in session.query(Pizza).all():
        add_calculatd_price(session, pizza)
        add_diet(session, pizza)

    session.close()