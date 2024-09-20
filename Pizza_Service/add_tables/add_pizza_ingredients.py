from sqlalchemy.orm import sessionmaker
from database import engine
from tables.pizza import Pizza
from tables.ingredient import Ingredient
from tables.pizza_ingredient import PizzaIngredient

Session = sessionmaker(bind=engine)
session = Session()

pizzas = {
    'margarita': session.query(Pizza).filter_by(name='margarita').first(),
    'pepperoni': session.query(Pizza).filter_by(name='pepperoni').first(),
    'hawaii': session.query(Pizza).filter_by(name='hawaii').first(),
    'four_cheese': session.query(Pizza).filter_by(name='four_cheese').first(),
    'bbq_chicken': session.query(Pizza).filter_by(name='bbq_chicken').first(),
    'veggie': session.query(Pizza).filter_by(name='veggie').first(),
    'meat_lovers': session.query(Pizza).filter_by(name='meat_lovers').first(),
    'buffalo_chicken': session.query(Pizza).filter_by(name='buffalo_chicken').first(),
    'spinach_feta': session.query(Pizza).filter_by(name='spinach_feta').first(),
    'truffle_mushroom': session.query(Pizza).filter_by(name='truffle_mushroom').first(),
}


mozzarella = session.query(Ingredient).filter_by(name='Mozzarella').first()
cheddar = session.query(Ingredient).filter_by(name='Cheddar').first()
parmesan = session.query(Ingredient).filter_by(name='Parmesan').first()
gorgonzola = session.query(Ingredient).filter_by(name='Gorgonzola').first()
feta = session.query(Ingredient).filter_by(name='Feta').first()
bell_peppers = session.query(Ingredient).filter_by(name='Bell Peppers').first()
onions = session.query(Ingredient).filter_by(name='Onions').first()
mushrooms = session.query(Ingredient).filter_by(name='Mushrooms').first()
olives = session.query(Ingredient).filter_by(name='Olives').first()
spinach = session.query(Ingredient).filter_by(name='Spinach').first()
artichokes = session.query(Ingredient).filter_by(name='Artichokes').first()
tomatoes = session.query(Ingredient).filter_by(name='Tomatoes').first()
chicken = session.query(Ingredient).filter_by(name='Chicken').first()
ham = session.query(Ingredient).filter_by(name='Ham').first()
pepperoni = session.query(Ingredient).filter_by(name='Pepperoni').first()
bacon = session.query(Ingredient).filter_by(name='Bacon').first()
sausage = session.query(Ingredient).filter_by(name='Sausage').first()
beef = session.query(Ingredient).filter_by(name='Beef').first()
salami = session.query(Ingredient).filter_by(name='Salami').first()
anchovies = session.query(Ingredient).filter_by(name='Anchovies').first()
bbq_sauce = session.query(Ingredient).filter_by(name='BBQ Sauce').first()
tomato_sauce = session.query(Ingredient).filter_by(name='Tomato Sauce').first()
pesto_sauce = session.query(Ingredient).filter_by(name='Pesto Sauce').first()
olive_oil = session.query(Ingredient).filter_by(name='Olive Oil').first()
garlic = session.query(Ingredient).filter_by(name='Garlic').first()
truffle_oil = session.query(Ingredient).filter_by(name='Truffle Oil').first()
pineapple = session.query(Ingredient).filter_by(name='Pineapple').first()
avocado = session.query(Ingredient).filter_by(name='Avocado').first()
sundried_tomatoes = session.query(Ingredient).filter_by(name='Sundried Tomatoes').first()
egg = session.query(Ingredient).filter_by(name='Egg').first()


def add_ingredients_to_pizza(pizza, ingredients):
    pizza_ingredients = []
    for ingredient, quantity in ingredients:
        pizza_ingredient = PizzaIngredient(pizza=pizza, ingredient=ingredient, quantity=quantity)
        session.add(pizza_ingredient)
        pizza_ingredients.append(pizza_ingredient)
    pizza.pizza_ingredients = pizza_ingredients



add_ingredients_to_pizza(pizzas['margarita'], [
    (mozzarella, 1),
    (tomato_sauce, 1)
])


add_ingredients_to_pizza(pizzas['pepperoni'], [
    (mozzarella, 1),
    (tomato_sauce, 1),
    (pepperoni, 1)
])


add_ingredients_to_pizza(pizzas['hawaii'], [
    (mozzarella, 1),
    (tomato_sauce, 1),
    (ham, 1),
    (pineapple, 1)
])


add_ingredients_to_pizza(pizzas['four_cheese'], [
    (mozzarella, 1),
    (cheddar, 1),
    (parmesan, 1),
    (feta, 1)
])


add_ingredients_to_pizza(pizzas['bbq_chicken'], [
    (bbq_sauce, 1),
    (chicken, 1),
    (onions, 1),
    (mozzarella, 1)
])


add_ingredients_to_pizza(pizzas['veggie'], [
    (bell_peppers, 1),
    (onions, 1),
    (mushrooms, 1),
    (olives, 1),
    (spinach, 1)
])


add_ingredients_to_pizza(pizzas['meat_lovers'], [
    (pepperoni, 1),
    (sausage, 1),
    (bacon, 1),
    (beef, 1),
    (salami, 1)
])


add_ingredients_to_pizza(pizzas['buffalo_chicken'], [
    (chicken, 1),
    (mozzarella, 1),
    (onions, 1),
    (bbq_sauce, 1)
])


add_ingredients_to_pizza(pizzas['spinach_feta'], [
    (spinach, 1),
    (feta, 1),
    (garlic, 1),
    (olive_oil, 1)
])


add_ingredients_to_pizza(pizzas['truffle_mushroom'], [
    (mushrooms, 1),
    (truffle_oil, 1),
    (parmesan, 1),
    (mozzarella, 1)
])


session.commit()


def calculate_price(pizza):
    return sum(ingredient.ingredient.price * ingredient.quantity for ingredient in pizza.pizza_ingredients)


def determine_diet(pizza):
    if all(ingredient.ingredient.diet == 'vegan' for ingredient in pizza.pizza_ingredients):
        return 'vegan'
    elif all(ingredient.ingredient.diet in ['vegan', 'vegetarian'] for ingredient in pizza.pizza_ingredients):
        return 'vegetarian'
    else:
        return ''


for pizza in pizzas.values():
    pizza.price = calculate_price(pizza)
    pizza.diet = determine_diet(pizza)


session.commit()

session.close()

print("Pizzas and ingredients added successfully!")
