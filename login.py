from Database.db import SessionLocal
from Database.Models.customer import CustomerAccount
from sqlalchemy import exists
from sqlalchemy.orm import Session
from register import register

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
    finally:
        session.close()
