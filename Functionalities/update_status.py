import sys
import os
import time

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from Database.Models.orders import Order
from Database.Models.delivery import DeliveryPerson
from datetime import datetime, timedelta

# Update order status method
def update_order_status(session: Session, order_id: int):
    """
    Update the status of an order based on its current state and timestamps.
    """
    order = session.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        return

    current_time = datetime.now()

    # If the order is being prepared and 10 minutes have passed, mark it as 'Out for delivery'
    if order.status in ["Being prepared", "Grouped for delivery"] and current_time >= order.order_time + timedelta(minutes=10):
        order.status = "Out for delivery"

    # If the order is out for delivery and the delivery time has passed, mark it as 'Delivered'
    if order.status == "Out for delivery" and current_time >= order.delivery_time:
        order.status = "Delivered"

        # After marking the order as delivered, handle the cooldown for the delivery person
        if order.delivery_person:
            delivery_person = order.delivery_person

            # Set the cooldown period so delivery driver can come back to the restaurant
            delivery_person.unavailable_until = current_time + timedelta(minutes=10)

    try:
        session.commit()
    except Exception as e:
        session.rollback()

