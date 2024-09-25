from login import login, register
from Database.db import SessionLocal
from datetime import date

# Testing register and login
with SessionLocal() as session:
    # Register a new customer
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

    # Register a second customer
    register(
        session=session,
        username="secondcustomer",
        password="password2001", 
        first_name="Second",
        last_name="Customer",
        gender="F",
        birthdate=date(1979, 2, 21),
        phone_number="987-653-321",
        address="Paul-Henri Spaaklaan 1, 6229 EN Maastricht"
    )

    # Should print "Invalid username or password."
    login(
        session=session,
        username="testuser",
        password="password2001"
    )

    # Should print "Invalid username or password."
    login(
         session=session,
         username="secondcustomer",
         password="hello123"
     )
    
    # Should print "Invalid username or password."
    login(
         session=session,
         username="No",
         password="Yes"
     )
    
    # Should print "Login succesful, welcome Test User!"
    login(
        session=session,
        username="testuser",
        password="hello123"
    )
    
    # Should print "Login succesful, welcome Second Customer!"
    login(
        session=session,
        username="secondcustomer",
        password="password2001"
    )
    session.close()