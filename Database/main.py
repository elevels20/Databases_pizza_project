from Database.db import init_db, SessionLocal
from Models import Customer, CustomerAccount  # Import other models as needed

# Initialize the database
init_db()

# Example usage:
session = SessionLocal()
new_customer = Customer(Name="John Doe", Gender="M", Birthdate="1990-01-01", PhoneNumber="1234567890")
session.add(new_customer)
session.commit()
