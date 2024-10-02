import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquirer
from Database.Models.orders import Order
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from Database.Models.customer import CustomerAccount

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

def cancel_order(session: Session, selected_order: Order, account: CustomerAccount):
    """
    Cancel an order if it's within 5 minutes of the order time.
    """
    try:
        if not selected_order:
            print("Order not found.")
            return

        # Check if the order belongs to the customer (via the account)
        if selected_order.customer_id != account.customer_id:
            print("You are not authorized to cancel this order.")
            return
        
        # Check if order has already been cancelled
        if selected_order.status == 'Cancelled':
            print("Order has already been cancelled.")
            return

        # Check if the order is within the 5-minute cancellation window
        current_time = datetime.now()
        if current_time > selected_order.order_time + timedelta(minutes=5):
            print("Cancellation period has expired. You cannot cancel this order.")
            return
        
        # Ask for confirmation to cancel the order
        questions = [
            inquirer.Confirm('confirm_cancel', message=f"Are you sure you want to cancel order {selected_order.order_id}?")
        ]
        confirmation = inquirer.prompt(questions)

        if not confirmation['confirm_cancel']:
            return "Order cancellation aborted."
        
        # Cancel the order
        selected_order.status = "Cancelled"
        session.commit()

        print(f"Order {selected_order.order_id} has been successfully cancelled.")
        return

    except Exception as e:
        session.rollback() 
        print(f"An error occurred while canceling the order: {e}")
        return