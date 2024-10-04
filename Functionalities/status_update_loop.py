import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from sqlalchemy.orm import Session
from Database.db import SessionLocal
from Functionalities.update_status import update_order_status
from Database.Models.orders import Order

def run_status_update_loop():
    try:
        while True:
            with SessionLocal() as session:
                # Fetch active orders
                active_orders = session.query(Order).filter(Order.status.in_(["Being prepared", "Out for delivery"])).all()

                # Update statuses only if there are active orders
                if active_orders:
                    for order in active_orders:
                        update_order_status(session, order.order_id)


            time.sleep(5)

    except Exception as e:
        pass
