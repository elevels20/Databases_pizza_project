import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from Database.Models.orders import Order
from Database.Models.delivery import DeliveryPerson
from datetime import datetime, timedelta

def update_order_status(session: Session, order_id: int):
    """
    Update the status of an order based on its current state and timestamps.
    """
    order = session.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        print(f"Order #{order_id} not found.")
        return

    current_time = datetime.now()
    # print(f"Current Time: {current_time}, Order Time: {order.order_time}, Delivery Time: {order.delivery_time}")

    # If the order is being prepared and 10 minutes have passed, mark it as 'Out for delivery'
    if order.status in ["Being prepared", "Grouped for delivery"] and current_time >= order.order_time + timedelta(seconds=30):
        order.status = "Out for delivery"
        # print(f"Order #{order_id} is now out for delivery.")

    # If the order is out for delivery and the delivery time has passed, mark it as 'Delivered'
    if order.status == "Out for delivery" and current_time >= order.delivery_time:
        order.status = "Delivered"
        # print(f"Order #{order_id} has been delivered.")

        # Make the delivery person available again
        if order.delivery_person:
            delivery_person = order.delivery_person
            delivery_person.availability = True
            delivery_person.unavailable_until = None
            # print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} is now available again.")

    # Commit the changes to the database
    session.commit()
