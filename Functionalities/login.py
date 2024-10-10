import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.db import SessionLocal
from Database.Models.customer import CustomerAccount, Customer
from sqlalchemy import exists
from sqlalchemy.orm import Session
from datetime import date

def login(session: Session, username: str, password: str) -> bool:
    """
    Customer login, check if username and password match.
    """
    try:
        account = session.query(CustomerAccount).filter(CustomerAccount.username == username, CustomerAccount.password == password).first()
        if account:
            print(f"Login succesful, welcome {account.customer.first_name} {account.customer.last_name}!")
            return True
        else:
            print("Invalid username or password.")
            return False
    except Exception as e:
        print(f"Error logging in customer {username}: {e}")
        return False

def register(session: Session, username: str, password: str, first_name: str, last_name: str, gender: str, birthdate: date, phone_number: str, country: str,  city: str, postal_code: str, street: str, house_number: int) -> bool:
    """
    Register a new customer and account to the database.
    """
    try:
        if session.query(exists().where(CustomerAccount.username == username)).scalar():
            print(f"Username {username} already exists.")
            return False
        else :
            new_customer = Customer(
                first_name = first_name,
                last_name = last_name,
                gender = gender,
                birthdate = birthdate,
                phone_number = phone_number,
                country = country,
                city = city,
                postal_code =postal_code,
                street = street,
                house_number = house_number
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
            return True
    except Exception as e:
        print(f"Error registering customer {first_name} {last_name}: {e}")
        return False