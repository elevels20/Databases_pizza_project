from datetime import date
from Database.db import SessionLocal
from Database.Models.customer import Customer, CustomerAccount
from sqlalchemy import exists
from sqlalchemy.orm import Session

def register(session: Session, username: str, password: str, first_name: str, last_name: str, gender: str, birthdate: date, phone_number: str, address: str) -> None:
    """
    Register a new customer and account to the database.
    """
    try:
        if session.query(exists().where(CustomerAccount.username == username)).scalar():
            print(f"Username {username} already exists.")
        else :
            new_customer = Customer(
                first_name = first_name, 
                last_name = last_name,
                gender = gender,
                birthdate = birthdate,
                phone_number = phone_number,
                address =address
                )
            new_customer_account = CustomerAccount(
                username = username,
                password = password,
                customer = new_customer
            )
            session.add(new_customer)
            session.add(new_customer_account)
            session.commit()
            print(f"Customer {first_name} {last_name} with username {username} registered.")
    except Exception as e:
        print(f"Error registering customer {first_name} {last_name}: {e}")
    finally:
        session.close()

