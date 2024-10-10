import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inquirer
from Functionalities.login import login, register
from Database.db import SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from Database.Models.customer import CustomerAccount

def login_inquirer(session: Session):
    """
    Login screen for terminal GUI.
    Returns CustomerAccount of registered/logged in customer and whether the account is an admin.
    """
    questions = [
        inquirer.List(
            'login',
            message='Welcome to our pizza service! Do you want to login or register?',
            choices=['Login', 'Register', 'Exit'],
        ),
    ]

    answers = inquirer.prompt(questions)

    if answers['login'] == 'Login':
        print("You chose: Login")
        questions = [
            inquirer.Text('username', message="Enter your username"),
            inquirer.Password('password', message="Enter your password"),
        ]

        answers = inquirer.prompt(questions)

        username = answers['username']
        password = answers['password']

        login(session,
              username=username,
              password=password
              )

        account = session.query(CustomerAccount).filter(CustomerAccount.username == username, CustomerAccount.password == password).first()

        if account and account.is_admin:
            print("Logged in as Admin.")
            return account, True  # Return True to indicate admin account
        elif account:
            print(f"Welcome {account.customer.first_name}!")
            return account, False
        else:
            print("Invalid credentials.")
            return None, False

    elif answers['login'] == 'Register':
        print("You chose: Register")
        questions = [
            inquirer.Text('username', message="Create a username"),
            inquirer.Password('password', message="Create a password"),
            inquirer.Text('first_name', message="What is your first name?"),
            inquirer.Text('last_name', message="What is your last name?"),
            inquirer.List('gender', message="What is your gender?", choices=['M', 'F']),
            inquirer.Text('birthdate', message="What is your date of birth? (YYYY-MM-DD)"),
            inquirer.Text('phone_number', message="What is your phone number?"),
            inquirer.Text('country', message="In what country do you live?"),
            inquirer.Text('city', message="In what city do you live?"),
            inquirer.Text('postal_code', message="What is your postal code?"),
            inquirer.Text('street', message="On what street do you live?"),
            inquirer.Text('house_number', message="What is your house number?"),
        ]

        answers = inquirer.prompt(questions)

        try:
            birthdate = datetime.strptime(answers['birthdate'], '%Y-%m-%d').date()
            username = answers['username']
            password = answers['password']
            registered = register(session,
                     username=username,
                     password=password,
                     first_name=answers['first_name'],
                     last_name=answers['last_name'],
                     gender=answers['gender'],
                     birthdate=birthdate,
                     phone_number=answers['phone_number'],
                     country=answers['country'],
                     city=answers['city'],
                     postal_code=answers['postal_code'],
                     street=answers['street'],
                     house_number=answers['house_number']
                     )
            
            if not registered:
                exit()
            account = session.query(CustomerAccount).filter(CustomerAccount.username == username, CustomerAccount.password == password).first()
            return account, False

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None, False

    elif answers['login'] == 'Exit':
        print("Exiting the pizza service!")
        exit()
        return None, False


def add_admin_account(session: Session):
    """
    Add an admin account during the database initialization.
    """
    admin_username = "admin"
    admin_password = "admin_password"  # You may hash this for better security

    existing_admin = session.query(CustomerAccount).filter_by(username=admin_username).first()

    if not existing_admin:
        from Database.Models.customer import Customer

        admin_customer = Customer(
            first_name="Admin",
            last_name="User",
            gender="F",
            birthdate="1970-01-01",
            phone_number='0000000000',
            address="Admin Address",
            postal_code="00000"
        )

        admin_account = CustomerAccount(
            username=admin_username,
            password=admin_password,
            customer=admin_customer,
            pizza_count=0,
            is_admin=True  # Mark the account as admin
        )

        session.add(admin_account)
        session.commit()

        print("Admin account created.")
    else:
        print("Admin account already exists.")
