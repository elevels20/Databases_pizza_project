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

    # If the order is being prepared and 30 seconds have passed, mark it as 'Out for delivery'
    if order.status in ["Being prepared", "Grouped for delivery"] and current_time >= order.order_time + timedelta(seconds=30):
        order.status = "Out for delivery"

    # If the order is out for delivery and the delivery time has passed, mark it as 'Delivered'
    if order.status == "Out for delivery" and current_time >= order.delivery_time:
        order.status = "Delivered"
        #print(f"Order #{order_id} has been delivered at {current_time}.")

        # After marking the order as delivered, handle the cooldown for the delivery person
        if order.delivery_person:
            delivery_person = order.delivery_person

            # Set the cooldown period (for testing, it's 20 seconds)
            delivery_person.unavailable_until = current_time + timedelta(seconds=20)
            #print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} will be available again after {delivery_person.unavailable_until}")

    # Commit the changes to the database
    try:
        session.commit()
    except Exception as e:
        session.rollback()


def check_delivery_person_availability(session: Session):
    """
    Checks and updates the availability of all delivery persons based on their cooldown status.
    """
    current_time = datetime.now()

    unavailable_delivery_persons = session.query(DeliveryPerson).filter(DeliveryPerson.unavailable_until.isnot(None)).all()

    for delivery_person in unavailable_delivery_persons:
        if delivery_person.unavailable_until <= current_time:
            delivery_person.availability = True
            delivery_person.unavailable_until = None
            print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} is now available.")


    try:
        session.commit()
    except Exception as e:
        session.rollback()

