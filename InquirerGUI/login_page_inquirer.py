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

def login_inquirer(session: Session) -> CustomerAccount:
    """
    Login screen for terminal GUI. 
    Returns CustomerAccount of registered/logged in customer.
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
            username = username,
            password = password
        )

        account = session.query(CustomerAccount).filter(CustomerAccount.username == username, CustomerAccount.password == password).first()
        return account
    
    elif answers['login'] == 'Register':
        print("You chose: Register")
        questions = [
            inquirer.Text('username', message="Create a username"),
            inquirer.Password('password', message="Create a password"),
            inquirer.Text('first_name', message="What is your first name?"),
            inquirer.Text('last_name', message="What is your last name?"),
            inquirer.List('gender', message="What is your gender?", choices=['M', 'F']),
            inquirer.Text('birthdate', message="What is date of birth? (YYYY-MM-DD)"),
            inquirer.Text('phone_number', message="What is your phone number?"),
            inquirer.Text('address', message="What is your address?"),
            inquirer.Text('postal_code', message="What's your postal code")
        ]

        answers = inquirer.prompt(questions)

        try:
            birthdate = datetime.strptime(answers['birthdate'], '%Y-%m-%d').date()
            username = answers['username']
            password = answers['password']
            register(session,
                username = username,
                password = password,
                first_name = answers['first_name'],
                last_name = answers['last_name'],
                gender = answers['gender'],
                birthdate = datetime.strptime(answers['birthdate'], '%Y-%m-%d').date(),
                phone_number = answers['phone_number'],
                address = answers['address'],
                postal_code= answers['postal_code']

            )
        
            account = session.query(CustomerAccount).filter(CustomerAccount.username == username, CustomerAccount.password == password).first()
            return account

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    elif answers['login'] == 'Exit':
        print("Exiting the pizza service!")
        # Code to handle 'Exit' action
        exit()
        return
