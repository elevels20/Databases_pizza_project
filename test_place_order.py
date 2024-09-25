from login import login, register
from Database.db import SessionLocal
from datetime import date
from Database.Models.menu import Pizza, Drink, Dessert
from place_order import place_order

# Create a customer account
with SessionLocal() as session:
    register(
        session=session,
        username="testuser",
        password="hello123", 
        first_name="Test",
        last_name="User",
        gender="M",
        birthdate=date(2000, 6, 13),
        phone_number="123-456-7890",
        address="Grote Looiersstraat 17, 6211 JH Maastricht"
    )

    pizza_order = [
        (session.query(Pizza).filter(Pizza.name == "Ham").first(), 2), 
        (session.query(Pizza).filter(Pizza.name == "Hawaii").first(), 1)
        ]
    drink_order = [
        (session.query(Drink).filter(Drink.name=="Coca cola").first(), 3)
    ]
    
    place_order(session, "testuser", pizza_order, drink_order)