from Database.db import SessionLocal, init_db
from Database.Models.customer import Customer

def main():
    # Initialize the database (create tables if not exists)
    init_db()

    # Create a new session
    session = SessionLocal()

    try:
        # Example query: Adding a new customer
        new_customer = Customer(Name="John Doe", Gender="M", Birthdate="1990-01-01", PhoneNumber="123456789", Address="123 Main St")
        session.add(new_customer)
        session.commit()

        added_customer = session.query(Customer).filter_by(Name="John Doe").first()
        if added_customer:
            print(f"Customer found in database: ID = {added_customer.CustomerID}, Name = {added_customer.Name}")
        else:
            print("Customer was not found in the database.")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    main()


