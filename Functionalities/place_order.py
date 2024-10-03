import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

        # Access the postal code through the related Customer object
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
            order_customer_account.total_pizza_count += quantity
            if not birthday_offer:
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
                
        if not birthday_offer:
            if discount_applied:
                total_price *= 0.9  # Apply a 10% discount
                print("Congratulations! You have received a 10% discount on this order.")

        if birthday_offer:
            new_order.total_price = 0
            new_order.birthday_order = True
            order_customer_account.birthday_offer_used_year = int(date.today().year)
        else:
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

    delivery_person = session.query(DeliveryPerson).join(PostalCodeArea).filter(
        PostalCodeArea.postal_code == postal_code,
        DeliveryPerson.availability == True
    ).first()

    if delivery_person:
        delivery_person.current_order_id = order.order_id
        delivery_person.availability = False
        order.delivery_person = delivery_person
        print(f"Delivery person {delivery_person.first_name} {delivery_person.last_name} assigned to order #{order.order_id}.")
    else:

        print(f"No available delivery person for postal code {postal_code}.")
        order.status = "Waiting for delivery"

    session.commit()


def group_orders_for_delivery(session: Session, new_order: Order):
    """
    Group orders for delivery based on postal code within a 3-minute window and a maximum batch of 3 pizzas.
    """
    postal_code = new_order.customer.postal_code
    three_minutes_ago = new_order.order_time - timedelta(minutes=3)

    grouped_orders = session.query(Order).join(Order.customer).filter(
        Order.customer.has(postal_code=postal_code),  # Use correct postal code filter
        Order.status == "Being prepared",
        Order.order_time >= three_minutes_ago,
        Order.order_id != new_order.order_id
    ).all()

    total_pizzas = sum(
        session.query(OrderPizza).filter(OrderPizza.order_id == order.order_id).count()
        for order in grouped_orders
    )
    total_pizzas += session.query(OrderPizza).filter(OrderPizza.order_id == new_order.order_id).count()

    if total_pizzas > 3:
        print(f"Cannot group orders. Total pizzas exceed the limit of 3.")
        return

    print(f"Orders #{', '.join([str(order.order_id) for order in grouped_orders])} will be grouped with Order #{new_order.order_id} for delivery.")
    new_order.status = "Grouped for delivery"

    for order in grouped_orders:
        order.status = "Grouped for delivery"

    session.commit()

