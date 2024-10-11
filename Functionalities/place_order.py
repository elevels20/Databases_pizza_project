import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Functionalities.discount_codes import apply_discount_code
from sqlalchemy.orm import Session
from typing import List, Tuple
from Database.Models.menu import Pizza, Drink, Dessert
from Database.Models.customer import CustomerAccount
from Database.Models.orders import Order, OrderPizza, OrderDessert, OrderDrink
from datetime import datetime, timedelta, date
from Database.Models.delivery import DeliveryPerson, PostalCodeArea

def place_order(session: Session, username: str, pizzas: List[Tuple[Pizza, int]], drinks: List[Tuple[Drink, int]] = None, desserts: List[Tuple[Dessert, int]] = None, birthday_offer: bool = False) -> Order:
    """
    Place an order for pizzas, drinks, and desserts. Each order must include at least one pizza.
    """
    if len(pizzas) < 1:
        print("Order must include at least one pizza.")
        return

    try:
        # Find the customer's account
        order_customer_account = session.query(CustomerAccount).filter(CustomerAccount.username == username).first()

        if not order_customer_account:
            print(f"Customer account for username '{username}' not found.")
            return


        customer_postal_code = order_customer_account.customer.postal_code

        total_price = 0
        current_time = datetime.now()

        # Create a new order
        new_order = Order(
            customer=order_customer_account.customer,
            status="Being prepared",  # Initial status
            order_time=current_time,
            total_price=total_price,
            delivery_time=current_time + timedelta(seconds=60),  # For testing, change to minutes later
        )
        if not birthday_offer:
            # Determine if a discount applies
            discount_applied = False
            if order_customer_account.discount_pizza_count >= 10:
                discount_applied = True
                order_customer_account.discount_pizza_count = 0

        # Add pizzas to the order
        for pizza, quantity in pizzas: 
            total_price = total_price + pizza.price * quantity
            session.add(OrderPizza(pizza=pizza, order=new_order, quantity=quantity))
            if not birthday_offer:
                order_customer_account.total_pizza_count += quantity
                order_customer_account.discount_pizza_count += quantity

        # Add drinks to the order if any
        if drinks is not None:
            for drink, quantity in drinks:
                total_price += drink.price * quantity
                session.add(OrderDrink(drink=drink, order=new_order, quantity=quantity))

        # Add desserts to the order if any
        if desserts is not None:
            for dessert, quantity in desserts:
                total_price += dessert.price * quantity
                session.add(OrderDessert(dessert=dessert, order=new_order, quantity=quantity))

        if birthday_offer:
            new_order.total_price = 0
            new_order.birthday_order = True
            order_customer_account.birthday_offer_used_year = int(date.today().year)
        else:
            if discount_applied:
                total_price *= 0.9  # Apply a 10% discount
                print("Congratulations! You have received a 10% discount on this order.")

            # Apply extra discount code if any
            total_price = apply_discount_code(session, order_customer_account, total_price)
            new_order.total_price = round(total_price, 2)

        session.add(new_order)
        session.commit()

        # Assign a delivery person after placing the order
        assign_delivery_person(session, new_order)

        print(f"Order #{new_order.order_id} is being prepared.")
        return new_order

    except Exception as e:
        session.rollback()
        print(f"Error placing order for {username}: {e}")
        return None


def assign_delivery_person(session: Session, order: Order):
    postal_code = order.customer.postal_code
    three_minutes_ago = datetime.now() - timedelta(minutes=3)
    MAX_PIZZAS_PER_DELIVERY = 3

    # Find recent orders within the same postal code and within 3 minutes
    recent_orders = session.query(Order).filter(
        Order.customer.has(postal_code=postal_code),
        Order.status.in_(["Being prepared", "Out for delivery"]),
        Order.order_time >= three_minutes_ago,
        Order.delivery_person_id.isnot(None)
    ).all()

    # Track how many pizzas each delivery person is handling
    delivery_person_pizza_count = {}

    for recent_order in recent_orders:
        delivery_person_id = recent_order.delivery_person_id
        if delivery_person_id not in delivery_person_pizza_count:
            delivery_person_pizza_count[delivery_person_id] = 0

        # Count pizzas in each order handled by the delivery person
        pizzas_in_order = session.query(OrderPizza).filter(OrderPizza.order_id == recent_order.order_id).all()
        total_pizzas = sum([pizza.quantity for pizza in pizzas_in_order])  # Correct pizza counting
        delivery_person_pizza_count[delivery_person_id] += total_pizzas

    # Calculate the number of pizzas in the new order
    pizzas_in_new_order = session.query(OrderPizza).filter(OrderPizza.order_id == order.order_id).all()
    new_order_pizza_count = sum([pizza.quantity for pizza in pizzas_in_new_order])  # Correct pizza counting

    # Check if we can group the new order with existing deliveries without exceeding the limit
    for delivery_person_id, total_pizzas_handled in delivery_person_pizza_count.items():
        # Check if the delivery person is not in cooldown
        delivery_person = session.query(DeliveryPerson).filter(DeliveryPerson.delivery_person_id == delivery_person_id).first()
        if delivery_person.unavailable_until is None or delivery_person.unavailable_until <= datetime.now():
            # Check if they can handle more pizzas without exceeding the maximum limit
            if total_pizzas_handled + new_order_pizza_count <= MAX_PIZZAS_PER_DELIVERY:
                order.delivery_person_id = delivery_person_id
                session.commit()
                return

    # If no grouping is possible, assign a new delivery person who is available and not in cooldown
    available_delivery_person = session.query(DeliveryPerson).join(PostalCodeArea).filter(
        PostalCodeArea.postal_code == postal_code,
        DeliveryPerson.availability == True,
        (DeliveryPerson.unavailable_until == None) | (DeliveryPerson.unavailable_until <= datetime.now())
    ).first()

    if available_delivery_person:
        available_delivery_person.current_order_id = order.order_id
        available_delivery_person.availability = False
        order.delivery_person = available_delivery_person
    else:
        order.status = "Waiting for delivery"

    session.commit()

