from sqlalchemy.orm import Session
from typing import List, Tuple
from Database.Models.menu import Pizza, Drink, Dessert
from Database.Models.customer import CustomerAccount
from Database.Models.orders import Order, OrderPizza, OrderDessert, OrderDrink
from datetime import datetime, timedelta

def place_order(session: Session, username: str, pizzas: List[Tuple[Pizza, int]], drinks: List[Tuple[Drink, int]] = None, desserts: List[Tuple[Dessert, int]] = None) -> Order:
    """
    Place an order for pizzas, drinks and desserts. Each order must include at least one pizza. 
    """
    if len(pizzas) < 1: # order must include at least one pizza
        print("Order must include at least one pizza.")
        return
    else:
        try: 
            order_customer_account = session.query(CustomerAccount).filter(CustomerAccount.username == username).first() # find the account of the customer who placed the order.
            total_price = 0
        
            current_time = datetime.now()

            new_order = Order(
                customer=order_customer_account.customer, 
                status="Being prepared", 
                order_time=current_time, 
                total_price=total_price, 
                delivery_time=current_time + timedelta(minutes=20),
                )
        
            for pizza, quantity in pizzas: 
                total_price = total_price + pizza.price * quantity
                session.add(OrderPizza(pizza=pizza, order=new_order, quantity=quantity))
                order_customer_account.pizza_count += quantity
        
            if drinks is not None:
                for drink, quantity in drinks:
                    total_price = total_price + drink.price * quantity
                    session.add(OrderDrink(drink=drink, order=new_order, quantity=quantity))


            if desserts is not None:
                for dessert, quantity in desserts:
                    total_price = total_price + dessert.price * quantity
                    session.add(OrderDessert(dessert=dessert, order=new_order, quantity=quantity))
        
            new_order.total_price = total_price
            session.add(new_order)
            session.commit()
            
            print(f"Order #{new_order.order_id} is being prepared.")
            return new_order
        except Exception as e:
            print(f"Error placing order of {username}: {e}")
