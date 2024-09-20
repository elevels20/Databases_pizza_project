from Database.db import SessionLocal, init_db
from Database.Models import Customer, Orders

def main():
    # Initialize the database (create tables if not exists)
    init_db()

    # Create a new session
    session = SessionLocal()

    # Example query: Adding a new customer
    new_customer = Customer(Name="John Doe", Gender="M", Birthdate="1990-01-01", PhoneNumber="123456789", Address="123 Main St")
    session.add(new_customer)
    session.commit()

if __name__ == "__main__":
    main()
