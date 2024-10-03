import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.Models.orders import Order
from Database.Models.menu import Pizza, Drink
from sqlalchemy.orm import Session
import inquirer


def log_out(session: Session):
    """
    Log out of GUI.
    """
    print("Logging out.")
    exit()

def print_order_details(selected_order: Order):
    """
    Print the details of an order.
    """
    print(f"""ORDER DETAILS: 
        Order ID: {selected_order.order_id}
        Status: {selected_order.status}
        Total price: {selected_order.total_price}
        Order time: {selected_order.order_time}
        Estimated delivery time: {selected_order.delivery_time}
    """)

    print("PIZZAS ORDERED: ")
    print(f"{'NAME':<20}{'QUANTITY':<10}{'DIET':<15}{'PRICE':<10}")
    for order_pizza in selected_order.order_pizzas: 
        price = order_pizza.quantity * order_pizza.pizza.price 
        diet = order_pizza.pizza.diet if order_pizza.pizza.diet else ""
        print(f"{order_pizza.pizza.name:<20}{order_pizza.quantity:<10}{diet:<15}{price:.2f}")

    if selected_order.order_desserts:
        print("\nDESSERTS ORDERED:")
        print(f"{'NAME':<20}{'QUANTITY':<10}{'DIET':<15}{'PRICE':<10}")
        for order_dessert in selected_order.order_desserts: 
            price = order_dessert.quantity * order_dessert.dessert.price 
            diet = order_dessert.dessert.diet if order_dessert.dessert.diet else ""
            print(f"{order_dessert.dessert.name:<20}{order_dessert.quantity:<10}{order_dessert.dessert.diet:<15}{price:.2f}")

    if selected_order.order_drinks:
        print("\nDRINKS ORDERED:")
        print(f"{'NAME':<20}{'QUANTITY':<10}{'PRICE':<10}")
        for order_drink in selected_order.order_drinks: 
            price = order_drink.quantity * order_drink.drink.price 
            print(f"{order_drink.drink.name:<20}{order_drink.quantity:<10}{price:.2f}")


def select_free_birthday_pizza(session: Session):
    """
    Let customer select a free pizza for their birthday.
    """
    try:
        # Retrieve all pizzas
        pizzas = session.query(Pizza).all()
        pizza_choices = [(pizza.name, pizza) for pizza in pizzas]
    except Exception as e:
        print(f"Error loading pizzas: {e}")
        return 
    
    questions = [
        inquirer.List('free_pizza', message="Select a free pizza:", choices=[name for name, _ in pizza_choices])
    ]
    answer = inquirer.prompt(questions)
    
    return next(pizza for name, pizza in pizza_choices if name == answer['free_pizza'])

def select_free_birthday_drink(session: Session):
    """
    Let customer select a free drink for their birthday.
    """
    try:
        # Retrieve all drinks
        drinks = session.query(Drink).all()
        drink_choices = [(drink.name, drink) for drink in drinks]
    except Exception as e:
        print(f"Error loading drinks: {e}")
        return     

    questions = [
        inquirer.List('free_drink', message="Select a free drink:", choices=[name for name, _ in drink_choices])
    ]
    answer = inquirer.prompt(questions)

    return next(drink for name, drink in drink_choices if name == answer['free_drink'])