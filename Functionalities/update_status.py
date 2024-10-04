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
        return

    current_time = datetime.now()

    # If the order is being prepared and 10 minutes have passed, mark it as 'Out for delivery'
    if order.status in ["Being prepared", "Grouped for delivery"] and current_time >= order.order_time + timedelta(seconds=30):
        order.status = "Out for delivery"

    # If the order is out for delivery and the delivery time has passed, mark it as 'Delivered'
    if order.status == "Out for delivery" and current_time >= order.delivery_time:
        order.status = "Delivered"

        # Make the delivery person available again
        if order.delivery_person:
            delivery_person = order.delivery_person
            delivery_person.availability = True
            delivery_person.unavailable_until = None

    # Commit the changes to the database
    try:
        session.commit()
    except Exception as e:
        session.rollback()
