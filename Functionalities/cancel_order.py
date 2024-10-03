import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquirer
from Database.Models.orders import Order
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from Database.Models.customer import CustomerAccount
from Database.Models.delivery import DeliveryPerson

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
            print("Order cancellation aborted.")
            return
        
        for order_pizza in selected_order.order_pizzas:
            pizza_quantity = order_pizza.quantity 
            account.total_pizza_count -= pizza_quantity

        # Reset birthday offer if it was a present
        if selected_order.birthday_order:
            account.birthday_offer_used_year = None
        else: 
            # Update total_pizza_count and discount_pizza_count for customer
            for order_pizza in selected_order.order_pizzas:
                pizza_quantity = order_pizza.quantity 
                account.discount_pizza_count -= pizza_quantity
        
        # Check in case counts got negative
        if account.total_pizza_count < 0:
            account.total_pizza_count = 0
        if account.discount_pizza_count < 0:
            account.discount_pizza_count = 0
            
        # Cancel the order
        selected_order.status = "Cancelled"

        # If a delivery person is assigned, make them available again
        if selected_order.delivery_person:
            delivery_person = selected_order.delivery_person
            delivery_person.availability = True
            delivery_person.unavailable_until = None  # Reset their unavailability timestamp if you have one
            print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} is now available again.")

        session.commit()

        print(f"Order {selected_order.order_id} has been successfully cancelled.")
        return

    except Exception as e:
        session.rollback()
        print(f"An error occurred while canceling the order: {e}")
        return
