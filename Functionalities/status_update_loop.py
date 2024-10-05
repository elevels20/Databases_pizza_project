import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from sqlalchemy.orm import Session
from Database.db import SessionLocal
from Functionalities.update_status import update_order_status
from Database.Models.orders import Order
from Database.Models.delivery import DeliveryPerson
from datetime import datetime

def run_status_update_loop():
    try:
        while True:
            with SessionLocal() as session:
                # Fetch active orders
                active_orders = session.query(Order).filter(Order.status.in_(["Being prepared", "Out for delivery"])).all()

                # Update order statuses
                if active_orders:
                    for order in active_orders:
                        update_order_status(session, order.order_id)

                # Check and update delivery person availability
                check_delivery_person_availability(session)

            time.sleep(5)  # Adjust the interval as needed

    except Exception as e:
        print(f"Error: {e}")
        pass

# Function to check delivery person's availability
def check_delivery_person_availability(session: Session):
    """
    Checks and updates the availability of all delivery persons based on their cooldown status.
    """
    current_time = datetime.now()

    # Query all delivery persons who are unavailable and check if their cooldown has expired
    unavailable_delivery_persons = session.query(DeliveryPerson).filter(DeliveryPerson.unavailable_until.isnot(None)).all()

    for delivery_person in unavailable_delivery_persons:
        if delivery_person.unavailable_until <= current_time:
            # Reset the availability of the delivery person
            delivery_person.availability = True
            delivery_person.unavailable_until = None
            #print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} is now available.")


    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error updating delivery person availability: {e}")
