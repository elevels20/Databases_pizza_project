import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.Models.orders import Order
from sqlalchemy.orm import Session
import time

def log_out(session: Session):
    """
    Log out of GUI.
    """
    print("Logging out.")
    exit()

def print_order_details(session: Session, order_id: int):
    """
    Print the details of an order, always fetching the latest version from the database.
    """
    # Re-fetch the order to ensure it is up to date
    selected_order = session.query(Order).filter(Order.order_id == order_id).first()

    if not selected_order:
        print(f"Order #{order_id} not found.")
        return

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